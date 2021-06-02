from tracklib.GestureClassifer import GestureClassifer
import numpy as np
import cv2 as cv

class Meanshift(GestureClassifer):
    def __init__(self, first_frame, init_loc: tuple):
        super().__init__()
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        self.term = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        self.loc = init_loc
        # a list to help deduce the last move you made 
        self.last_rois = [self.loc]
        # get first frame
        self.roi = first_frame[self.loc[1]:self.loc[1] + self.loc[3], self.loc[0]:self.loc[0] + self.loc[2]]
        self.roi_hist = self.get_histogram()

    def get_histogram(self):
        hsv_roi = cv.cvtColor(self.roi, cv.COLOR_BGR2HSV)
        # get histogram of hue for Back Projection
        mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        return cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)

    def run(self, frame):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # find the same object with Back Projection based on histogram
        dst = cv.calcBackProject([hsv_frame], [0], self.roi_hist, [0, 180], 1)
        # apply meanshift to get the new location
        _, self.loc = cv.meanShift(dst, self.loc, self.term)
        self.last_rois.append(self.loc)
        # set the maximum length of the list to 10 elements
        if len(self.last_rois) > 10:
            del self.last_rois[0]
        # recognize gesture and replace it with the assigned number
        gesture = self.classify_with_coords(self.last_rois, frame)
        return gesture

    def draw(self, frame):
        # method for debugging, to show camera view
        img = cv.rectangle(frame, (self.loc[0], self.loc[1]), (self.loc[0] + self.loc[2], self.loc[1] + self.loc[3]), 255, 2)
        cv.imshow('img', img)
        cv.waitKey(30) & 0xff

    def update_view(self, frame, loc):
        # if the glove is lost, reset the initial values 
        self.loc = loc
        self.last_rois = [self.loc]
        self.roi = frame[self.loc[1]:self.loc[1] + self.loc[3], self.loc[0]:self.loc[0] + self.loc[2]]
        self.roi_hist = self.get_histogram()


class Camshift(Meanshift):
    # extended version of the camshift algorithm with the ability to change the size of roi
    def run(self, frame):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # find the same object with Back Projection based on histogram
        dst = cv.calcBackProject([hsv_frame], [0], self.roi_hist, [0, 180], 1)
        # apply meanshift to get the new location
        _, self.loc = cv.CamShift(dst, self.loc, self.term)
        self.last_rois.append(self.loc)
        # set the maximum length of the list to 10 elements
        if len(self.last_rois) > 10:
            del self.last_rois[0]
        gesture = self.classify_with_coords(self.last_rois, frame)
        return gesture


class OpticalFlow(GestureClassifer):
    def __init__(self, first_frame, init_loc):
        super().__init__()
        self.lk_params = dict(winSize=(20, 20), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        self.prev_frame_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
        self.prev_point = np.array([[init_loc[0] + init_loc[2] // 2, init_loc[1] + init_loc[3] // 2]], dtype=np.float32)
        # a list to help deduce the last move you made
        self.prev_points = [tuple(map(int, self.prev_point[0]))]

    def run(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # calculate optical flow
        self.prev_point, _, _ = cv.calcOpticalFlowPyrLK(self.prev_frame_gray, frame_gray, self.prev_point, None, **self.lk_params)
        # save as previous params
        self.prev_frame_gray = frame_gray
        self.prev_points.append(tuple(map(int, self.prev_point[0])))
        # set the maximum length of the list to 10 elements
        if len(self.prev_points) > 10:
            del self.prev_points[0]
        color = self.classify_with_point(self.prev_points, frame)
        return color

    def draw(self, frame):
        # method for debugging, to show camera view
        # draw tracked circle
        rpoint = self.prev_point.ravel()
        frame = cv.circle(frame, (int(rpoint[0]), int(rpoint[1])), 5, (240, 255, 255), -1)
        cv.imshow('frame', frame)
        cv.waitKey(30) & 0xff

    def update_view(self, frame, loc):
        # if the glove is lost, reset the initial values 
        self.prev_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.prev_point = np.array([[loc[0] + loc[2] // 2, loc[1] + loc[3] // 2]], dtype=np.float32)
        self.prev_points = [tuple(self.prev_point[0])]


class TemplateMatching(GestureClassifer):
    METHODS = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    def __init__(self, first_frame, init_loc, method='cv.TM_CCOEFF'):
        super().__init__()
        # current location
        self.loc = init_loc
        # a list to help deduce the last move you made 
        self.last_matching = [self.loc]
        self.template = first_frame[self.loc[1]:self.loc[1] + self.loc[3], self.loc[0]:self.loc[0] + self.loc[2]]
        if method in TemplateMatching.METHODS:
            self.method = eval(method)
        else:
            self.method = cv.TM_CCOEFF

    def run(self, frame):
        res = cv.matchTemplate(frame, self.template, self.method)
        _, _, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if self.method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            x, y = min_loc
        else:
            x, y = max_loc
        location = (x, y, x + self.loc[2], y + self.loc[3])
        self.last_matching.append(location)
        # set the maximum length of the list to 10 elements
        if len(self.last_matching) > 10:
            del self.last_matching[0]
        gesture = self.classify_with_coords(self.last_matching, frame)
        return gesture

    def draw(self, frame):
        # method for debugging, to show camera view
        location = self.last_matching[-1]
        frame = cv.rectangle(frame, (location[0], location[1]), (location[2], location[3]), 255, 2)
        cv.imshow('frame', frame)
        cv.waitKey(30) & 0xff

    def update_view(self, frame, loc):
        # if the glove is lost, reset the initial values 
        self.loc = loc
        self.last_matching = [self.loc]
        self.template = frame[self.loc[1]:self.loc[1] + self.loc[3], self.loc[0]:self.loc[0] + self.loc[2]]
