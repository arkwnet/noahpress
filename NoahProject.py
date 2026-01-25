import NoahCommon

class Project:
    def __init__(self):
        self.version = "20260125"
        self.w = 257
        self.h = 364
        self.unit = "mm"
        self.dpi = 600
        self.zoom = 10
        self.data = []

    def get_width_px(self):
        if self.unit == "px":
            return self.w
        elif self.unit == "mm":
            return int(self.w * self.dpi / NoahCommon.ONE_INCH_MM)
        else:
            return

    def get_height_px(self):
        if self.unit == "px":
            return self.h
        elif self.unit == "mm":
            return int(self.h * self.dpi / NoahCommon.ONE_INCH_MM)
        else:
            return

    def pixel_zoom(self, px):
        return int(px * (self.zoom / 100))
