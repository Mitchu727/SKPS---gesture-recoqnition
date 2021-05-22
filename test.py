import numpy as np
import cv2 as cv
from algorithms.MeanShift import MeanShift

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


# TODO
num = 1
cap = cv.VideoCapture(f'vtest/vtest_{num}.mp4')
# loc_str = open("vtest/vtest_loc.txt", "r").readlines()[num - 1]
# loc = tuple(map(int, loc_str.split(', ')))

if cap.isOpened():
    _, frame = cap.read()
    loc = find_pink(frame)
    meanshift = MeanShift(frame, loc)

while cap.isOpened():
    _, frame = cap.read()
    print(meanshift.algorithm(frame))
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
