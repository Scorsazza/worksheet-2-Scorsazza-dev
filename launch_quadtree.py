import pyasge

from game.quadtrees import MyASGEGame


def main():
    # setup the game settings first
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.WINDOWED
    settings.vsync = pyasge.Vsync.DISABLED

    # start the game
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
