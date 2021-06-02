import numpy as np

class GestureClassifer:
    def __init__(self, classify_quan=10):
        self.classify_quan = classify_quan
        self.classify_error = 25

    def classify_with_coords(self, last_rois, frame):
        # for algorithms with region of interest
        # in our implementation for: Meanshift, Camshift and Template Matching
        sample = last_rois[-self.classify_quan:]
        diff_height_index, diff_height = self.height_change(sample)
        diff_width_index, diff_width = self.width_change(sample)
        # if the object moved more than the assumed error to detect any suspected situation that glove is lost
        if diff_height > self.classify_error or diff_width > self.classify_error:
            return self.choose_gesture(diff_height_index, diff_height, diff_width_index, diff_width)
        else:
            color = self.get_dominant_color(frame[sample[-1][1]:sample[-1][1] + sample[-1][3], sample[-1][0]:sample[-1][0] + sample[-1][2]])
            # if pink
            if 255 > color[2] > 128 and 209 > color[1] > 3 and 220 > color[0] > 40:
                return 0  # stay in this localization
            else:
                return None  # find glove

    def classify_with_point(self, last_points, frame):
        # for algorithms with point of interest
        # in our implementation for: Optical Flow
        sample = last_points[-self.classify_quan:]
        diff_height_index, diff_height = self.height_change(sample)
        diff_width_index, diff_width = self.width_change(sample)
        # if the object moved more than the assumed error to detect any suspected situation that glove is lost
        if diff_height > self.classify_error or diff_width > self.classify_error:
            return self.choose_gesture(diff_height_index, diff_height, diff_width_index, diff_width)
        elif sample[-1][1] <= frame.shape[0] and sample[-1][0] <= frame.shape[1]:
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

    def height_change(self, sample):
        # get the extremes of height to find out how much your hand moved
        min_height = min(sample, key=lambda x: x[1])
        max_height = max(sample, key=lambda x: x[1])
        # get index of that extremas to find out which direction your hand moved
        min_height_index = sample.index(min_height)
        max_height_index = sample.index(max_height)

        diff_height_index = max_height_index - min_height_index
        diff_height = max_height[1] - min_height[1]
        return diff_height_index, diff_height

    def width_change(self, sample):
        # get the extremes of width to find out how much your hand moved
        min_width = min(sample, key=lambda x: x[0])
        max_width = max(sample, key=lambda x: x[0])
        # get index of that extremas to find out which direction your hand moved
        min_width_index = sample.index(min_width)
        max_width_index = sample.index(max_width)

        diff_width_index = max_width_index - min_width_index
        diff_width = max_width[0] - min_width[0]
        return diff_width_index, diff_width

    def choose_gesture(self, diff_height_index, diff_height, diff_width_index, diff_width):
        if diff_height > diff_width:
            if diff_height_index > 0:
                # downward movement
                return 1
            else:
                # upward movement
                return 2
        else:
            if diff_width_index > 0:
                # right movement
                return 3
            else:
                # left movement
                return 4
