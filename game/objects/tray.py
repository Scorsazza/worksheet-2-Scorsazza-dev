from game.gamedata import SUB_ROTATION_BOUND_OFFSET
from game.objects.submission import Submission


class Tray:
    def __init__(self, x, y, w, h, number, filename):
        self.number = number
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.example = Submission(0, x + int(w / 4), y + int(h / 4), number, number, filename)

    def centre(self):
        return (self.x + int(self.w / 2)), (self.y + int(self.h / 2))

    def inside(self, sprite):
        bs = sprite.getWorldBounds()
        if bs.v1.x < (self.x + self.w + SUB_ROTATION_BOUND_OFFSET) and bs.v2.x > (self.x - SUB_ROTATION_BOUND_OFFSET):
            if bs.v3.y < (self.y + self.h + SUB_ROTATION_BOUND_OFFSET) and bs.v1.y > (
                    self.y - SUB_ROTATION_BOUND_OFFSET):
                return True
        return False

    def valid(self, sub, mode):
        if mode == 0:
            if sub.colour == self.number:
                return True
        else:
            if sub.number == self.number:
                return True
        return False

    def render(self, renderer):
        self.example.render(renderer)