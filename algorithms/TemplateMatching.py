import cv2 as cv
import numpy as np

class TemplateMatching:
    METHODS = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    def __init__(self, first_frame, init_loc, method='cv.TM_CCOEFF'):
        self.loc = init_loc
        self.template = first_frame[self.loc[1]:self.loc[1] + self.loc[3], self.loc[0]:self.loc[0] + self.loc[2]]
        if method in TemplateMatching.METHODS:
            self.method = eval(method)
        else:
            self.method = cv.TM_CCOEFF

    def run(self, frame):
        res = cv.matchTemplate(frame, self.template, self.method)
        self.draw(frame, res)

    def draw(self, frame, res):
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if self.method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + self.loc[2], top_left[1] + self.loc[3])
        frame = cv.rectangle(frame, top_left, bottom_right, 255, 2)
        cv.imshow('frame', frame)
        cv.waitKey(30) & 0xff
