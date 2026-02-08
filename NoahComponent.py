COMPONENT_RECTANGLE = 10

class Box:
    def __init__(self, mode, x, y, w, h, fill):
        self.status = 0
        self.mode = mode
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fill = fill
        self.select = 1
