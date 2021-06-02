import cv2 as cv
import numpy as np

from tracklib.algorithms import Camshift, Meanshift, OpticalFlow, TemplateMatching
from tracklib.ColorPicker import ColorPicker

class Tracker:
    def __init__(self, video, algorithm="Meanshift"):
        self.init_loc, frame = self.find_pink_glove(video)
        self.algorithm = self.choose_algorithm(algorithm, frame)
        self.color = ColorPicker()

    def find_pink_glove(self, video: cv.VideoCapture):
        # algorithm which is trying to find pink glove - tracked object in our implementation
        loc = None
        while loc is None:
            _, frame = video.read()
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            upper_range = np.array([359, 255, 255])
            lower_range = np.array([100, 100, 100])
            mask = cv.inRange(hsv, lower_range, upper_range)
            pink_contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

            if len(pink_contours) > 0:
                pink_area = max(pink_contours, key=cv.contourArea)
                loc = cv.boundingRect(pink_area)
        return loc, frame

    def update_init_loc(self, video: cv.VideoCapture):
        # called when the tracked object is lost
        self.init_loc, frame = self.find_pink_glove(video)
        self.algorithm.update_view(frame, self.init_loc)

    def choose_algorithm(self, algorithm, frame):
        if algorithm == "Meanshift":
            return Meanshift(frame, self.init_loc)
        elif algorithm == "Camshift":
            return Camshift(frame, self.init_loc)
        elif algorithm == "OpticalFlow":
            return OpticalFlow(frame, self.init_loc)
        elif algorithm == "TemplateMatching":
            return TemplateMatching(frame, self.init_loc)

    def change_algorithm(self, algorithm, video):
        self.init_loc, frame = self.find_pink_glove(video)
        self.algorithm = self.choose_algorithm(algorithm, frame)
        print(f"Current algorithm {self.algorithm.__class__.__name__}")
