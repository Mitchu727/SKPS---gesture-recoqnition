import cv2 as cv
from tracklib.Tracker import Tracker

path = "vtest/vtest.mp4"
alg = "Meanshift"

cap = cv.VideoCapture("vtest/vtest.mp4")
# cap.set(cv.CAP_PROP_FPS, 10)
if cap.isOpened():
    tracker = Tracker(cap, algorithm=alg)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if int(cap.get(cv.CAP_PROP_POS_FRAMES)) % 5 == 0:
        gesture = tracker.algorithm.run(frame)
        print(gesture)
        color = tracker.color.convert_gesture(gesture)
        cv.waitKey(1)
cap.release()
cv.destroyAllWindows()

# python -m profile video_analyz.py
