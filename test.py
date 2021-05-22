import numpy as np
import cv2 as cv
from algorithms.Tracker import Tracker

def find_pink(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    upper_range = np.array([359, 255, 255])
    lower_range = np.array([100, 100, 100])
    mask = cv.inRange(hsv, lower_range, upper_range)
    pink_contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

    if len(pink_contours) > 0:
        pink_area = max(pink_contours, key=cv.contourArea)
        loc = cv.boundingRect(pink_area)
        return loc

path = input("Enter path: ")
if path == "":
    path = "vtest/vtest_1.mp4"

cap = cv.VideoCapture(path)
if cap.isOpened():
    # create tracker with chosen algorithm
    tracker = Tracker(cap)
while cap.isOpened():
    # read frame and run step of algorithm
    _, frame = cap.read()
    color = tracker.algorithm.run(frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
