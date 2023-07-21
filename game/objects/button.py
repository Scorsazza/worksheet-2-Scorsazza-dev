import pyasge


class Button:
    def __init__(self, states, x, y, w, h):
        self.idx = 0
        self.wait = 0

        self.sprites = []
        for i in range(2):
            self.sprites.append(pyasge.Sprite())
            self.sprites[i].loadTexture(states[i])
            self.sprites[i].loadTexture(states[i])
            self.sprites[i].x = x
            self.sprites[i].y = y
            self.sprites[i].width = w
            self.sprites[i].height = h

    def press(self):
        self.idx = 1

    def release(self):
        self.idx = 0

    def clicked(self, x, y):
        sprite = self.sprites[self.idx]
        if sprite.x < x < (sprite.x + sprite.width):
            if sprite.y < y < (sprite.y + sprite.height):
                self.press()
                self.wait = 0.1
                return True
        return False

    def update(self, delta_time):
        if self.wait > 0:
            self.wait = self.wait - delta_time
            if self.wait <= 0:
                self.release()
                self.wait = 0

    def render(self, renderer):
        renderer.render(self.sprites[self.idx])
