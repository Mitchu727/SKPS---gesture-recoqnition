import colorsys

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


class ColorPicker:
    HUE_MAX = 360
    HUE_MIN = 0
    SATURATION_MAX = 100
    SATURATION_MIN = 0
    VALUE_MAX = 100
    VALUE_MIN = 0

    def __init__(self):
        self.__hue = 180
        self.__saturation = 100
        self.__value = 50
        self.changer = 1

    @property
    def changer(self):
        return self._changer

    @changer.setter
    def changer(self, value):
        if value > 0:
            self._changer = value

    def add_hue(self):
        hue = self.__hue + self.changer
        if hue > ColorPicker.HUE_MAX:
            self.__hue = ColorPicker.HUE_MAX
        else:
            self.__hue = hue

    def sub_hue(self):
        hue = self.__hue - self.changer
        if hue < ColorPicker.HUE_MIN:
            self.__hue = ColorPicker.HUE_MIN
        else:
            self.__hue = hue

    def add_value(self):
        value = self.__value + self.changer
        if value > ColorPicker.VALUE_MAX:
            self.__value = ColorPicker.VALUE_MAX
        else:
            self.__value = value

    def sub_value(self):
        value = self.__value - self.changer
        if value < ColorPicker.VALUE_MIN:
            self.__value = ColorPicker.VALUE_MIN
        else:
            self.__value = value

    def __normalize(self, value, min_val, max_val):
        return (value - min_val) / (max_val - min_val)

    def get_hex(self):
        # hsv to 0,1 scale
        n_hue = self.__normalize(self.__hue, ColorPicker.HUE_MIN, ColorPicker.HUE_MAX)
        n_saturation = self.__normalize(self.__saturation, ColorPicker.SATURATION_MIN, ColorPicker.SATURATION_MAX)
        n_value = self.__normalize(self.__value, ColorPicker.VALUE_MIN, ColorPicker.VALUE_MAX)
        # hsv 0,1 scaled to rgb
        rgb_color = [int(color * 255)for color in list(colorsys.hsv_to_rgb(n_hue, n_saturation, n_value))]
        # rgb to hex
        return "#" + "".join([f"{v:02x}" for v in rgb_color])
