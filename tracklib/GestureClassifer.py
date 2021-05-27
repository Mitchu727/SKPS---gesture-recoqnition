import numpy as np
from timers import clock_timer, time_timer, timeit_timer


class GestureClassifer:
    def __init__(self, classify_quan=10):
        self.classify_quan = classify_quan
        self.classify_error = 50

    def classify_with_coords(self, last_rois, frame):
        sample = last_rois[-self.classify_quan:]
        diff_hight_index, diff_hight = self.hight_change(sample)
        diff_width_index, diff_width = self.width_change(sample)
        if diff_hight > self.classify_error or diff_width > self.classify_error:
            return self.choose_gesture(diff_hight_index, diff_hight, diff_width_index, diff_width)
        else:
            color = self.get_dominant_color(frame[sample[-1][1]:sample[-1][1] + sample[-1][3], sample[-1][0]:sample[-1][0] + sample[-1][2]])
            # if pink
            if 255 > color[2] > 128 and 209 > color[1] > 3 and 220 > color[0] > 40:
                return 0  # stay in this localization
            else:
                return None  # find glove

    @clock_timer
    def run(self, frame, *args):
        color = self.detect(frame)
        # self.draw(frame)
        return color

    def classify_with_point(self, last_points, frame):
        sample = last_points[-self.classify_quan:]
        diff_hight_index, diff_hight = self.hight_change(sample)
        diff_width_index, diff_width = self.width_change(sample)
        if diff_hight > self.classify_error or diff_width > self.classify_error:
            return self.choose_gesture(diff_hight_index, diff_hight, diff_width_index, diff_width)
        else:
            color = frame[sample[-1][1]][sample[-1][0]]
            # if pink
            if 255 > color[2] > 128 and 209 > color[1] > 3 and 220 > color[0] > 40:
                return 0  # stay in this localization
            else:
                return None  # find glove

    def get_dominant_color(self, frame):
        col_max = (256, 256, 256)  # RGB
        frame_1D = np.ravel_multi_index(frame.reshape(-1, frame.shape[-1]).T, col_max)
        return np.unravel_index(np.bincount(frame_1D).argmax(), col_max)

    def hight_change(self, sample):
        min_hight = min(sample, key=lambda x: x[1])
        max_hight = max(sample, key=lambda x: x[1])

        min_hight_index = sample.index(min_hight)
        max_hight_index = sample.index(max_hight)

        diff_hight_index = max_hight_index - min_hight_index
        diff_hight = max_hight[1] - min_hight[1]
        return diff_hight_index, diff_hight

    def width_change(self, sample):
        min_width = min(sample, key=lambda x: x[0])
        max_width = max(sample, key=lambda x: x[0])

        min_width_index = sample.index(min_width)
        max_width_index = sample.index(max_width)

        diff_width_index = max_width_index - min_width_index
        diff_width = max_width[0] - min_width[0]
        return diff_width_index, diff_width

    def choose_gesture(self, diff_hight_index, diff_hight, diff_width_index, diff_width):
        if diff_hight > diff_width:
            if diff_hight_index > 0:
                return 1
            else:
                return 2
        else:
            if diff_width_index > 0:
                return 3
            else:
                return 4
