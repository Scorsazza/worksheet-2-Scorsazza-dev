import pyasge
import json
from game.gamedata import GameData
from tasks.task2_sort import sort


class HighScoreTableWidget:
    game_data = None    # Shared game data and services
    headers = []        # Table headings
    score_data = None   # List of all the scores [score, name]
    table_font = None   # The font used for the table headings

    def __init__(self, shared_data: GameData):
        self.game_data = shared_data
        self.table_font = self.game_data.renderer.loadFont("/data/fonts/emulogic.ttf", 52)

        # Title for the widget
        self.menu_title = pyasge.Text(self.table_font)
        self.menu_title.string = "SUBMISSIONS PLEASE \n   HALL OF FAME"
        self.menu_title.x = 350
        self.menu_title.y = 100
        self.menu_title.scale = 1
        self.fade_out = True

        # Timer to ensure scores are displayed for a certain time
        self.display_timer = 0

        # Setup table headers and load the JSON data
        self.init_headers()
        self.reload()

    def init_headers(self) -> None:
        self.headers.append(pyasge.Text(self.game_data.fonts["scores"], "RANK"))
        self.headers.append(pyasge.Text(self.game_data.fonts["scores"], "DESIGNATION"))
        self.headers.append(pyasge.Text(self.game_data.fonts["scores"], "SCORE"))
        for header in self.headers:
            header.y = 300

        self.headers[0].x = 400
        self.headers[1].x = 600
        self.headers[2].x = 1000

    def reload(self) -> None:
        scores = open("./data/scores/scores.json", "rt")
        self.score_data = json.loads(scores.read())
        scores.close()

    def dump(self) -> None:
        scores = open("./data/scores/scores.json", "wt")
        scores.write(json.dumps(self.score_data))
        scores.close()

    def add(self, score: int, name: str) -> None:
        self.score_data.append((score, name))
        self.score_data = sort(self.score_data)
        # Start the timer for how long the scores should be displayed
        self.display_timer = 3

    def key_handler(self, event: pyasge.KeyEvent) -> bool:
        if self.display_timer <= 0:
            self.display_timer = 0;
            if event.action == 0:
                return True
        return False

    def update(self, game_time: pyasge.GameTime) -> None:
        if self.display_timer > 0:
            self.display_timer -= game_time.fixed_timestep

    def render(self, game_time: pyasge.GameTime) -> None:
        self.render_title(game_time)
        self.render_headings()
        self.render_scores()

    def render_headings(self) -> None:
        for heading in self.headers:
            self.game_data.renderer.render(heading)

    def render_title(self, game_time: pyasge.GameTime) -> None:
        if self.fade_out:
            self.menu_title.opacity -= 0.75 * game_time.frame_time
            if self.menu_title.opacity <= 0:
                self.fade_out = False
        else:
            self.menu_title.opacity += 0.75 * game_time.frame_time
            if self.menu_title.opacity >= 1:
                self.fade_out = True
        self.game_data.renderer.render(self.menu_title)

    def render_scores(self) -> None:
        for count, score in enumerate(self.score_data):
            if count == 10:
                break

            rank_txt = pyasge.Text(self.game_data.fonts["scores"], str(count + 1))
            rank_txt.y = 350 + (50 * count)
            rank_txt.x = 400
            self.game_data.renderer.render(rank_txt)

            name_txt = pyasge.Text(self.game_data.fonts["scores"])
            name_txt.string = score[1]
            name_txt.x = 600
            name_txt.y = 350 + (50 * count)
            self.game_data.renderer.render(name_txt)

            score_txt = pyasge.Text(self.game_data.fonts["scores"])
            score_txt.string = str(score[0]).zfill(8)
            score_txt.y = 350 + (50 * count)
            score_txt.x = 1000
            score_txt.colour = pyasge.COLOURS.HOTPINK
            self.game_data.renderer.render(score_txt)
