import numpy as np
import cv2 as cv
from algorithms.MeanShift import MeanShift

# TODO
num = 2
cap = cv.VideoCapture(f'vtest/vtest_{num}.mp4')
loc_str = open("vtest/vtest_loc.txt", "r").readlines()[num - 1]
loc = tuple(map(int, loc_str.split(', ')))

if cap.isOpened():
    meanshift = MeanShift(cap, loc)

while cap.isOpened():
    _, frame = cap.read()
    print(meanshift.algorithm(frame))
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
