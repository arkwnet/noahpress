class Mouse:
    def __init__(self, status, x, y, i):
        self.status = status
        self.x = x
        self.y = y
        self.i = i

class Box:
    def __init__(self, x, y, w, h, active):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.active = active
