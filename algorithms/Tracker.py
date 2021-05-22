from algorithms.MeanShift import MeanShift
import cv2 as cv
import numpy as np

class Tracker:
    def __init__(self, video):
        _, frame = video.read()
        init_loc = self.find_pink_glove(frame)
        self.algorithm = MeanShift(frame, init_loc)

    def find_pink_glove(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        upper_range = np.array([359, 255, 255])
        lower_range = np.array([100, 100, 100])
        mask = cv.inRange(hsv, lower_range, upper_range)
        pink_contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

        if len(pink_contours) > 0:
            pink_area = max(pink_contours, key=cv.contourArea)
            loc = cv.boundingRect(pink_area)
            return loc
