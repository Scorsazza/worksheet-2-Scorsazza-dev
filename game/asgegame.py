import pyasge
from pyasge import Texture
from pyfmodex.flags import MODE
from data.scores.generate_scores import generate_random_scores
from game.gamedata import GameData
from game.scenes.gamestates import GameState
from game.scenes.highscore import HighScoreTableWidget
from game.scenes.score_input import UserInputWidget
from game.scenes.gameplay import GamePlayState

MENU_BG_VOLUME = 0.75
GAME_BG_VOLUME = 0.25


class MyASGEGame(pyasge.ASGEGame):
    backgrounds = []  # parallax scrolling backgrounds
    game_state = GameState.ATTRACT_SCREEN  # the starting game state
    score = 0  # used to track the player score

    def __init__(self, settings: pyasge.GameSettings):

        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.CORNFLOWER)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # give us some scores
        generate_random_scores()

        # background audio
        self.data.audio_system.init()

        self.bg_audio = (
            self.data.audio_system.create_sound("./data/audio/industrial.mp3", mode=MODE.LOOP_NORMAL)).play()
        self.fade_bg_audio(0.0, MENU_BG_VOLUME, 1)

        # setup the background and load the fonts for the game
        self.init_background()
        self.init_fonts()

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_handler)
        self.mousemove_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.move_handler)

        # create the score input and high table widgets
        self.score_input = UserInputWidget(self.data)
        self.high_scores = HighScoreTableWidget(self.data)
        self.game = GamePlayState(self.data)

        # mouse cursor
        self.cursor = pyasge.Sprite()
        self.init_cursor()

    def init_cursor(self):
        self.cursor.loadTexture("./data/img/cursors.png")
        self.cursor.width = 16
        self.cursor.height = 16
        self.cursor.src_rect[2] = 16
        self.cursor.src_rect[3] = 16
        self.cursor.scale = 4
        self.cursor.z_order = 127
        self.cursor.colour = pyasge.COLOURS.SEAGREEN
        self.cursor.setMagFilter(pyasge.MagFilter.NEAREST)
        self.inputs.setCursorMode(pyasge.CursorMode.HIDDEN)

    def init_fonts(self) -> None:
        self.data.fonts["title"] = self.data.renderer.loadFont("/data/fonts/emulogic.ttf", 52)
        self.data.fonts["text"] = self.data.renderer.loadFont("/data/fonts/emulogic.ttf", 28)
        self.data.fonts["scores"] = self.data.renderer.loadFont("/data/fonts/emulogic.ttf", 28)
        self.data.fonts["tiny"] = self.data.renderer.loadFont("/data/fonts/emulogic.ttf", 9)

    def init_background(self) -> None:
        for i in range(4):
            self.backgrounds.append(pyasge.Sprite())
            self.backgrounds[i].loadTexture(f"./data/img/bg{i}.png")
            self.backgrounds[i].setMagFilter(pyasge.MagFilter.NEAREST)
            self.backgrounds[i].width = 1600
            self.backgrounds[i].height = 900
            self.backgrounds[i].z_order = -100 + i
            self.backgrounds[i].texture.setUVMode(Texture.UVWrapMode.REPEAT, Texture.UVWrapMode.REPEAT)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if self.game_state == GameState.GAME_SCREEN:
            self.game.click_handler(event)

    def move_handler(self, event: pyasge.ClickEvent) -> None:
        self.cursor.x = event.x
        self.cursor.y = event.y

        if self.game_state == GameState.GAME_SCREEN:
            self.game.move_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.key == pyasge.KEYS.KEY_ESCAPE:
            self.backgrounds = []
            self.bg_audio.stop()
            self.signalExit()

        elif self.game_state == GameState.ATTRACT_SCREEN:
            if event.action == pyasge.KEYS.KEY_PRESSED:
                if event.key == pyasge.KEYS.KEY_ENTER:
                    self.game_state = GameState.INPUT_SCREEN

        elif self.game_state == GameState.INPUT_SCREEN:
            self.score_input.key_handler(event)

        elif self.game_state == GameState.GAME_SCREEN:
            if event.action == pyasge.KEYS.KEY_PRESSED:
                if event.key == pyasge.KEYS.KEY_BACKSPACE:
                    self.game.timer = 0

        elif self.game_state == GameState.HIGH_SCORE_SCREEN:
            if self.high_scores.key_handler(event):
                self.game_state = GameState.ATTRACT_SCREEN
                self.game.reset()

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        if self.game_state != GameState.GAME_SCREEN:
            self.backgrounds[1].src_rect[0] = (self.backgrounds[1].src_rect[0] + 2 * game_time.fixed_timestep)
            self.backgrounds[2].src_rect[0] = (self.backgrounds[2].src_rect[0] + 15 * game_time.fixed_timestep)
            self.backgrounds[3].src_rect[0] = (self.backgrounds[3].src_rect[0] + 30 * game_time.fixed_timestep)

    def update(self, game_time: pyasge.GameTime) -> None:
        if self.game_state == GameState.ATTRACT_SCREEN:
            pass

        elif self.game_state == GameState.INPUT_SCREEN:
            finished, self.data.name = self.score_input.update()
            if finished:
                self.game_state = GameState.GAME_SCREEN
                self.game.update_designation()
                self.data.audio_system.create_sound("./data/audio/8-bit-kit-boop_C.wav").play()
                self.fade_bg_audio(MENU_BG_VOLUME, GAME_BG_VOLUME, 1)

        elif self.game_state == GameState.GAME_SCREEN:
            running, self.score = self.game.update(game_time)
            if not running:
                self.high_scores.add(self.score, self.data.name)
                self.game_state = GameState.HIGH_SCORE_SCREEN
                self.bg_audio.pitch = 1.0
                self.fade_bg_audio(GAME_BG_VOLUME, MENU_BG_VOLUME, 1)

        elif self.game_state == GameState.HIGH_SCORE_SCREEN:
            self.high_scores.update(game_time)

        else:
            pyasge.ERROR(f"{self.game_state}: update not supported!")

    def render(self, game_time: pyasge.GameTime) -> None:
        self.renderer.render(self.cursor)

        if self.game_state == GameState.ATTRACT_SCREEN:
            for bg in self.backgrounds:
                self.renderer.render(bg)
            start_game = pyasge.Text(self.data.fonts["title"], "PRESS START")
            start_game.colour = pyasge.COLOURS.HOTPINK
            start_game.y = 400
            start_game.x = 550
            self.renderer.render(start_game)

            menu_title = pyasge.Text(self.data.fonts["title"], "SUBMISSIONS PLEASE")
            menu_title.x = 400
            menu_title.y = 300
            menu_title.scale = 1
            self.renderer.render(menu_title)

        elif self.game_state == GameState.GAME_SCREEN:
            for bg in self.backgrounds:
                self.renderer.render(bg)
            self.game.render(game_time)

        elif self.game_state == GameState.INPUT_SCREEN:
            for bg in self.backgrounds:
                self.renderer.render(bg)
            self.score_input.render()

        elif self.game_state == GameState.HIGH_SCORE_SCREEN:
            for bg in self.backgrounds:
                self.renderer.render(bg)
            self.high_scores.render(game_time)

        else:
            pyasge.ERROR(f"{self.game_state}: render not supported!")

    def fade_bg_audio(self, start_volume: float, end_volume: float, time: float):
        clock = self.bg_audio.dsp_clock.dsp_clock
        freq = self.bg_audio.frequency
        self.bg_audio.add_fade_point(clock, start_volume)
        self.bg_audio.add_fade_point(clock + int(freq * time), end_volume)
