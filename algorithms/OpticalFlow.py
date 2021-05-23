import numpy as np
import cv2 as cv
from algorithms.GestureClassifer import GestureClassifer

class OpticalFlow(GestureClassifer):
    def __init__(self, first_frame, init_loc):
        super().__init__()
        self.lk_params = dict(winSize=(20, 20), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        self.prev_frame_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
        self.prev_point = np.array([[init_loc[0] + init_loc[2] // 2, init_loc[1] + init_loc[3] // 2]], dtype=np.float32)
        self.last_rois = [tuple(self.prev_point[0])]

    def run(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # calculate optical flow
        self.prev_point, st, err = cv.calcOpticalFlowPyrLK(self.prev_frame_gray, frame_gray, self.prev_point, None, **self.lk_params)
        # save as previous params
        self.prev_frame_gray = frame_gray
        self.last_rois.append(tuple(self.prev_point[0]))
        color = self.classify(self.last_rois)
        self.draw(frame)
        return color

    def draw(self, frame):
        # draw tracked circle
        rpoint = self.prev_point.ravel()
        frame = cv.circle(frame, (int(rpoint[0]), int(rpoint[1])), 5, (240, 255, 255), -1)
        cv.imshow('frame', frame)
        cv.waitKey(30) & 0xff

    def update_view(self, frame, loc):
        self.prev_frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.prev_point = np.array([[loc[0] + loc[2] // 2, loc[1] + loc[3] // 2]], dtype=np.float32)
        self.last_rois = [tuple(self.prev_point[0])]
