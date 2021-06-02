import cv2 as cv
from tracklib.Tracker import Tracker
import time

path = "vtest/vtest1.mp4"
alg = "OpticalFlow"

gestures = []
cap = cv.VideoCapture(path)
cap.set(cv.CAP_PROP_FPS, 10)
start = time.time()
frame_numerator = 0
if cap.isOpened():
    tracker = Tracker(cap, algorithm=alg)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if int(cap.get(cv.CAP_PROP_POS_FRAMES)) % 1 == 0:
        gesture = tracker.algorithm.run(frame)
        gestures.append(gesture)
        color = tracker.color.convert_gesture(gesture)
        print(gestures)
        tracker.algorithm.draw(frame)
        cv.waitKey(1)
        frame_numerator += 1
end = time.time()
print(frame_numerator / (end - start))
cap.release()
cv.destroyAllWindows()
print(gestures)

# python -m profile video_analyz.py
