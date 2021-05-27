import cv2 as cv
from tracklib.Tracker import Tracker
from timers import delog
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = "vtest/vtest.mp4"
    open('data.txt', 'w').close()
    algorithms = ["Meanshift", "Camshift", "TemplateMatching", "OpticalFlow"]
    # algorithms = ["OpticalFlow"]
    for alg in algorithms:
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
        with open('data.txt', 'a+') as f:
            f.write("\n")
    data = delog()
    for i, line in enumerate(data):
        plt.plot([i for i in range(len(line))], line, label=algorithms[i])
    plt.legend()
    plt.show()
    cv.destroyAllWindows()
