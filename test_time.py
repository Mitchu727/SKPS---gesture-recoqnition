import time
import cv2 as cv
from tracklib.Tracker import Tracker


if __name__ == "__main__":
    path = "vtest/vtest.mp4"
    for alg in ["Meanshift"]:
        numerator = 1
        cap = cv.VideoCapture(path)
        if cap.isOpened():
            tracker = Tracker(cap, algorithm=alg)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # gesture = tracker.algorithm.run(frame)
            # color = tracker.color.convert_gesture(gesture)
            tracker.algorithm.run(frame)
        cap.release()
    cv.destroyAllWindows()
