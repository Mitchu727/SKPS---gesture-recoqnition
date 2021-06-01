import colorsys

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
        self.changer = 10

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

    def convert_gesture(self, gest_num):
        if gest_num is None:
            return "LookingFor"
        if gest_num == 1:
            self.sub_value()
        elif gest_num == 2:
            self.add_value()
        elif gest_num == 3:
            self.add_hue()
        elif gest_num == 4:
            self.sub_hue()
        return self.get_hex()
