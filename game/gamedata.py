import math

# constants used throughout the game
import pyfmodex

SUBMISSION_WIDTH = 100
SUBMISSION_HEIGHT = 100
SUB_ROTATION_BOUND = 0.349
SUB_ROTATION_BOUND_OFFSET = math.sin(SUB_ROTATION_BOUND) * max(SUBMISSION_WIDTH, SUBMISSION_HEIGHT)


class GameData:
    """ GameData stores the data that needs to be shared

    When using multiple states in a game, you will find that
    some game data needs to be shared. GameData can be used to
    share access to data that a the game and running states may
    need.
    """

    def __init__(self) -> None:
        self.audio_system = pyfmodex.System()
        self.background = None
        self.fonts = {}
        self.game_res = [0, 0]
        self.inputs = None
        self.name = ""
        self.renderer = None
        self.score = 0
