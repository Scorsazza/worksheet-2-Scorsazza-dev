import random
import pyasge


class Person:
    def __init__(self, index: int, x: int, y: int):
        self.sprite = pyasge.Sprite()
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.loadTexture(f"./data/img/p_{random.randint(0, 27)}.png")
        self.sprite.setMagFilter(pyasge.MagFilter.LINEAR)
        self.sprite.z_order = index

    def update(self, delta_time):
        pass

    def render(self, renderer):
        renderer.render(self.sprite)
