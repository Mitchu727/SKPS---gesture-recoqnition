from algorithms.ColorPicker import ColorPicker

class GestureClassifer:
    def __init__(self, classify_quan=30):
        self.classify_quan = classify_quan
        self.color = ColorPicker()

    def classify(self, last_rois):
        sample = last_rois[-self.classify_quan:]
        diff_hight_index, diff_hight = self.hight_change(sample)
        diff_width_index, diff_width = self.width_change(sample)
        self.choose_gesture(diff_hight_index, diff_hight, diff_width_index, diff_width)
        return self.color.get_hex()

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
                self.color.sub_value()
            else:
                self.color.add_value()
        else:
            if diff_width_index > 0:
                self.color.add_hue()
            else:
                self.color.sub_hue()
