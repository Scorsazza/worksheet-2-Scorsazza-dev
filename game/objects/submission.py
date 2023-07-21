import pyasge
import random
from game.gamedata import SUBMISSION_WIDTH
from game.gamedata import SUBMISSION_HEIGHT
from game.gamedata import SUB_ROTATION_BOUND


class Submission:
    def __init__(self, index, x=979, y=535, colour=-1, number=-1, filename=""):
        if colour == -1:
            self.colour = random.randint(0, 2)
        else:
            self.colour = colour
        if number == -1:
            self.number = random.randint(0, 2)
        else:
            self.number = number

        self.sprite = pyasge.Sprite()
        self.init_texture(filename, index, x, y)

    def init_texture(self, filename, index, x, y):
        if len(filename) > 0:
            self.sprite.loadTexture(filename)
        else:
            self.sprite.loadTexture(f"./data/img/sub_{self.colour}_{self.number}.png")

        self.sprite.x = x
        self.sprite.y = y
        self.sprite.width = SUBMISSION_WIDTH
        self.sprite.height = SUBMISSION_HEIGHT
        self.sprite.setMagFilter(pyasge.MagFilter.LINEAR)
        self.sprite.z_order = index
        self.sprite.rotation = random.uniform(-SUB_ROTATION_BOUND, SUB_ROTATION_BOUND)

    def update(self, delta_time):
        pass

    def reset(self):
        self.sprite.x = 979
        self.sprite.y = 535

    def render(self,  renderer):
        renderer.render(self.sprite)
