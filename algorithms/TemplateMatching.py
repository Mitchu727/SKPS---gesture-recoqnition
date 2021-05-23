from algorithms.GestureClassifer import GestureClassifer
import cv2 as cv
import numpy as np

class TemplateMatching(GestureClassifer):
    METHODS = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    def __init__(self, first_frame, init_loc, method='cv.TM_CCOEFF'):
        super().__init__()
        self.loc = init_loc
        self.last_matching = [self.loc]
        self.template = first_frame[self.loc[1]:self.loc[1] + self.loc[3], self.loc[0]:self.loc[0] + self.loc[2]]
        if method in TemplateMatching.METHODS:
            self.method = eval(method)
        else:
            self.method = cv.TM_CCOEFF

    def run(self, frame):
        res = cv.matchTemplate(frame, self.template, self.method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if self.method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            x, y = min_loc
        else:
            x, y = max_loc
        location = (x, y, x + self.loc[2], y + self.loc[3])
        self.last_matching.append(location)
        color = self.classify(self.last_matching)
        self.draw(frame, location)
        return color

    def draw(self, frame, location):
        frame = cv.rectangle(frame, (location[0], location[1]), (location[2], location[3]), 255, 2)
        cv.imshow('frame', frame)
        cv.waitKey(30) & 0xff
