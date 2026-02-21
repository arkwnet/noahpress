COMPONENT_RECTANGLE = 10
COMPONENT_TEXT = 20

class Box:
    def __init__(self, mode, x, y, w, h, fill, obj):
        self.status = 0
        self.mode = mode
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fill = fill
        self.obj = obj
        self.select = 0

class Text:
    def __init__(self, body, font, size):
        self.status = 0
        self.body = body
        self.font = font
        self.size = size
