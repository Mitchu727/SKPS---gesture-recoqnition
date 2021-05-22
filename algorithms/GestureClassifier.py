class GestureClassifer:
    def __init__(self, classify_quan=30):
        self.classify_quan = classify_quan

    def classify(self, last_rois):
        sample = last_rois[-self.classify_quan:]

        min_hight = min(sample, key=lambda x: x[1])
        max_hight = max(sample, key=lambda x: x[1])

        min_hight_index = sample.index(min_hight)
        max_hight_index = sample.index(max_hight)

        diff_hight_index = max_hight_index - min_hight_index
        diff_hight = max_hight[1] - min_hight[1]

        min_width = min(sample, key=lambda x: x[0])
        max_width = max(sample, key=lambda x: x[0])

        min_width_index = sample.index(min_width)
        max_width_index = sample.index(max_width)

        diff_width_index = max_width_index - min_width_index
        diff_width = max_width[0] - min_width[0]

        self.choose_gesture(diff_hight_index, diff_hight, diff_width_index, diff_width)

    def choose_gesture(self, diff_hight_index, diff_hight, diff_width_index, diff_width):
        print(diff_hight_index, diff_hight, diff_width_index, diff_width)
        if diff_hight > diff_width:
            if diff_hight_index > 0:
                print("Down")
            else:
                print("Up")
        else:
            if diff_width_index > 0:
                print("Right")
            else:
                print("Left")
