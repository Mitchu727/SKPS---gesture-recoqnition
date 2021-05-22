import numpy as np
import cv2 as cv
from MeanShift import MeanShift

# TODO
num = 2
cap = cv.VideoCapture(f'vtest_{num}.mp4')
loc_str = open("vtest_loc.txt", "r").readlines()[num - 1]
loc = tuple(map(int, loc_str.split(', ')))

while cap.isOpened():
    meanshift = MeanShift(cap, loc)
    meanshift.algorithm()
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
