from algorithms.MeanShift import MeanShift
import cv2 as cv

class Camshift(MeanShift):
    def run(self, frame):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # find the same object with Back Projection based on histogram
        dst = cv.calcBackProject([hsv_frame], [0], self.roi_hist, [0, 180], 1)
        # apply meanshift to get the new location
        _, self.loc = cv.CamShift(dst, self.loc, self.term)
        self.last_rois.append(self.loc)
        color = self.classify(self.last_rois)
        self.draw(frame)
        return color
