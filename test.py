import numpy as np
import cv2 as cv
from MeanShift import MeanShift

cap = cv.VideoCapture('vtest.mp4')
while cap.isOpened():
    meanshift = MeanShift(cap, (300, 200, 100, 50))
    meanshift.algorithm()
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
