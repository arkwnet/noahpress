import NoahCommon

class Project:
    def __init__(self):
        self.version = "20260322"
        self.w = 257
        self.h = 364
        self.unit = "mm"
        self.dpi = 600
        self.zoom = 10
        self.data = []

    def get_width_px(self):
        return self.mm_to_px(self.w)

    def get_height_px(self):
        return self.mm_to_px(self.h)

    def mm_to_px(self, i):
        if self.unit == "px":
            return i
        elif self.unit == "mm":
            return int(i * self.dpi / NoahCommon.ONE_INCH_MM)

    def px_to_mm(self, i):
        return int(i / self.dpi * NoahCommon.ONE_INCH_MM)

    def pixel_zoom(self, px):
        return int(px * (self.zoom / 100))
