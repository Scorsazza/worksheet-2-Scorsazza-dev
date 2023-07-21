import sys
import pyasge
from game.asgegame import MyASGEGame
from pathlib import Path

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)


def main():
    # setup the game settings first
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.DISABLED

    # start the game
    game = MyASGEGame(settings)
    game.run()
    game.high_scores.dump()


if __name__ == "__main__":
    main()
