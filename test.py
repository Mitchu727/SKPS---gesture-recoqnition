import numpy as np
import cv2 as cv
from algorithms.Tracker import Tracker


# path = input("Enter path: ")
# if path == "":
path = "vtest/vtest_2.mp4"

cap = cv.VideoCapture(path)
if cap.isOpened():
    # create tracker with chosen algorithm
    tracker = Tracker(cap, algorithm="OpticalFlow")
while cap.isOpened():
    # read frame and run step of algorithm
    _, frame = cap.read()
    color = tracker.algorithm.run(frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
