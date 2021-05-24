import cv2 as cv
from tracklib.Tracker import Tracker
import timeit

# @pytest.mark.parametrize("path, alg, correctness", [("vtest/vtest.mp4", "Meanshift", correct)])
def test_effectiveness(path: str, alg: str, correctness: list):
    cap = cv.VideoCapture(path)
    cap.set(cv.CAP_PROP_FPS, 10)
    score = 0
    if cap.isOpened():
        tracker = Tracker(cap, algorithm=alg)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gesture = tracker.algorithm.run(frame)
        if gesture == correctness[i]:
            score += 1
        i += 1
        cv.waitKey(100)
    cap.release()
    cv.destroyAllWindows()
    percent = score / len(correctness) * 100
    return percent

def test_efficiency(path: str, alg: str):
    return timeit.timeit(lambda: run_alogirthm(path, alg), number=5) / 5

def run_alogirthm(path, alg):
    cap = cv.VideoCapture(path)
    cap.set(cv.CAP_PROP_FPS, 10)
    if cap.isOpened():
        tracker = Tracker(cap, algorithm=alg)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gesture = tracker.algorithm.run(frame)
        color = tracker.color.convert_gesture(gesture)
        cv.waitKey(100)
    cap.release()
    cv.destroyAllWindows()

f = open("vtest/vcheck.txt", "r")
vcheck = f.readline().split(",")[1:]
correct = []
for check in vcheck:
    if check.strip() == "None":
        correct.append(None)
    else:
        correct.append(int(check))

effectivness = {}
efficiency = {}
algorithms = ["Meanshift", "TemplateMatching", "OpticalFlow", "Camshift"]
for algorithm in algorithms:
    efficiency[algorithm] = test_efficiency("vtest/vtest.mp4", algorithm)
    effectivness[algorithm] = test_effectiveness("vtest/vtest.mp4", algorithm, correct)
print(effectivness, efficiency)
