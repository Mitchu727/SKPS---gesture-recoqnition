class GestureClassifer:
    def __init__(self, classify_quan=5):
        self.classify_quan = classify_quan

    def classify(self, last_rois):
        print(last_rois[-self.classify_quan:])
