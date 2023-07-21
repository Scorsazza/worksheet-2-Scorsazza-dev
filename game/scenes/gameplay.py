import pyasge
import random

from game.objects.button import Button
from game.gamedata import GameData, SUB_ROTATION_BOUND_OFFSET, SUBMISSION_HEIGHT, SUBMISSION_WIDTH
from game.objects.person import Person
from game.objects.submission import Submission
from game.objects.tray import Tray
from tasks.task1_queue import Queue
from tasks.task1_stack import Stack

# these constants allow the game parameters to be easily adjusted.
TRAY_WIDTH = 100
START_TIME = 10
SUCCESS_TIME_INC = 5
FAIL_TIME_DEC = 2
MAX_PEOPLE = int(1344 / 64)
X_MARGIN = 130
PEOPLE_MARGIN = 75


def submission_bounds():
    return [
        979 - SUB_ROTATION_BOUND_OFFSET, 535 - SUB_ROTATION_BOUND_OFFSET,
        SUBMISSION_WIDTH + SUB_ROTATION_BOUND_OFFSET, SUBMISSION_HEIGHT + SUB_ROTATION_BOUND_OFFSET
    ]


def is_inside(bounds, x, y):
    if bounds[0] <= x <= (bounds[0] + bounds[2]):
        if bounds[1] <= y <= (bounds[1] + bounds[3]):
            return True
    return False


def intersects(sprite1, sprite2):
    bs = sprite1.getWorldBounds()
    bb = sprite2.getWorldBounds()
    if bs.v1.x < bb.v2.x and bs.v2.x > bb.v1.x:
        if bs.v3.y > bb.v1.y and bs.v1.y < bb.v3.y:
            return True
    return False


class GamePlayState:
    game_data = None  # Shared game data and services

    def __init__(self, shared_data: GameData):
        self.game_data = shared_data
        self.desk = pyasge.Sprite()
        self.init_desk()

        self.active_person = None
        self.clicked = False
        self.mode = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.next_btn = Button(["./data/img/next.png", "./data/img/nextPressed.png"], 190, 610, 210, 105)
        self.people = Queue()
        self.people_add = 2
        self.score = 0
        self.spawn_timer = 0
        self.sub_index = 0
        self.submission = None
        self.submissions = Stack()
        self.timer = START_TIME
        self.total_people = 0

        self.submission_trays = []
        self.submission_trays.append(Tray(1337, 227, 190, 180, 0, f"./data/img/SubR.png"))
        self.submission_trays.append(Tray(1337, 452, 190, 180, 1, f"./data/img/SubG.png"))
        self.submission_trays.append(Tray(1337, 673, 190, 180, 2, f"./data/img/SubB.png"))

        self.submission_modes = []
        self.submission_modes.append(pyasge.Text(self.game_data.fonts["scores"], "Colours", 10, 802, pyasge.COLOURS.HOTPINK))
        self.submission_modes.append(pyasge.Text(self.game_data.fonts["scores"], "Numbers", 379, 802, pyasge.COLOURS.SLATEGRAY))
        self.reset_mode()

        # Initialise game ui text
        self.scoreboard = pyasge.Text(self.game_data.fonts["scores"])
        self.designation = pyasge.Text(self.game_data.fonts["scores"])
        self.timer_clock = pyasge.Text(self.game_data.fonts["scores"])
        self.warning = pyasge.Text(self.game_data.fonts["scores"])
        self.warning_fade_mode = 0
        self.init_ui()

        # load "next" sound sample and store as channel [0]
        self.next_sound = self.game_data.audio_system.create_sound("./data/audio/next.mp3")
        self.nope_sound = self.game_data.audio_system.create_sound("./data/audio/8-bit-shot_F#_minor.wav")
        self.channels = [self.next_sound.play(paused=True), self.nope_sound.play(paused=True)]

    def init_ui(self):
        self.scoreboard.string = str(self.score).zfill(8)
        self.scoreboard.y = 30
        self.scoreboard.x = 600
        self.scoreboard.colour = pyasge.COLOURS.WHITE

        self.designation.y = 30
        self.designation.x = 1125
        self.designation.colour = pyasge.COLOURS.HOTPINK

        self.timer_clock.string = str("{:.1f}".format(self.timer))
        self.timer_clock.y = 30
        self.timer_clock.x = 50
        self.timer_clock.colour = pyasge.COLOURS.WHITE

        self.warning.string = "   WARNING!\nQUEUE OVERLOAD"
        self.warning.colour = pyasge.COLOURS.GREENYELLOW
        self.warning.x = 100
        self.warning.y = 205

    def reset(self):
        self.mode = 0
        self.people_add = 2
        self.score = 0
        self.spawn_timer = 0
        self.sub_index = 0
        self.timer = START_TIME
        self.total_people = 0
        self.submission = None
        self.submissions = Stack()
        self.active_person = None
        self.clicked = False
        self.people = Queue()
        self.reset_mode()
        self.scoreboard.string = str(self.score).zfill(8)

    def init_desk(self):
        self.desk.loadTexture(f"./data/img/desk1.png")
        self.desk.setMagFilter(pyasge.MagFilter.NEAREST)
        self.desk.width = int(self.desk.width)
        self.desk.height = int(self.desk.height)
        self.desk.x = 0
        self.desk.y = 177
        self.desk.z_order = -1

    def update_designation(self) -> None:
        self.designation.string = "DESIGNATION: " + self.game_data.name[0:3]

    def submission_selected(self, x: int, y: int) -> bool:
        bounds = submission_bounds()
        if is_inside(bounds, x, y):
            self.submission = self.submissions.pop()
            return True
        return False

    def next_clicked_check(self, x: float, y: float) -> bool:
        return self.next_btn.clicked(x, y)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.action == 1 and event.button == 0:
            if self.submission_selected(event.x, event.y):
                self.clicked = True  # trigger the submission as selected

            if self.next_clicked_check(event.x, event.y):
                self.call_next_person()

        if self.clicked:
            if event.action == 0 and event.button == 0:
                self.handle_btn_release()

    def handle_btn_release(self) -> None:
        # check to see if submission is on tray
        for tray in self.submission_trays:
            if self.submission is not None:
                if tray.inside(self.submission.sprite):
                    if tray.valid(self.submission, self.mode):
                        # well done, it's the right tray
                        self.score += 100
                        self.scoreboard.string = str(self.score).zfill(8)
                        self.timer = self.timer + SUCCESS_TIME_INC

                        if self.timer > 10:
                            # reset the colour of the timer
                            self.timer_clock.colour = pyasge.COLOURS.LIMEGREEN
                    else:
                        #  oh no, this is not right
                        self.timer = self.timer - FAIL_TIME_DEC

                        if self.channels[1].current_sound:
                            self.channels[1].stop()

                        # play the audio sample
                        self.channels[1] = self.nope_sound.play()
                        self.channels[1] .volume = 0.5

                    # reset the game mode and drop the submission
                    self.reset_mode()
                    self.submission = None

        if self.submission is not None:  # This means it is not over a tray, so push back onto the stack
            self.submission.reset()
            self.submissions.push(self.submission)
            self.submission = None

    def reset_mode(self) -> None:
        self.mode = random.randint(0, 1)
        self.submission_modes[self.mode].colour = pyasge.COLOURS.HOTPINK
        self.submission_modes[self.mode].opacity = 1
        self.submission_modes[1 - self.mode].colour = pyasge.COLOURS.LIGHTSLATEGRAY
        self.submission_modes[1 - self.mode].opacity = 0.1

    def call_next_person(self) -> None:
        self.active_person = self.people.dequeue()

        if self.active_person is not None:
            for i in range(random.randint(1, 5)):
                self.submissions.push(Submission(self.sub_index))
                self.sub_index += 1

            # reposition existing people in the queue
            for person in range(self.people.len()):
                self.people.at(person).sprite.x += PEOPLE_MARGIN

            # set person's position to front of desk
            self.active_person.sprite.x = 65
            self.active_person.sprite.y = 235
            self.active_person.sprite.width = 450
            self.active_person.sprite.height = 300
            self.active_person.sprite.z_order = -2
            self.active_person.sprite.setMagFilter(pyasge.MagFilter.NEAREST)

            # don't double the samples
            if self.channels[0].current_sound:
                self.channels[0].stop()

            # play audio when calling next person up
            self.channels[0] = self.next_sound.play()
            self.channels[0].volume = 2

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        self.mouse_x = event.x
        self.mouse_y = event.y

    def update(self, game_time: pyasge.GameTime) -> (bool, int):
        if self.submission is not None:
            self.submission.sprite.x = self.mouse_x - int(self.submission.sprite.width / 2)
            self.submission.sprite.y = self.mouse_y - int(self.submission.sprite.height / 2)

        self.update_spawn_timer(game_time)
        self.next_btn.update(game_time.fixed_timestep)

        for i in range(self.people.len()):
            self.people.at(i).update(game_time.frame_time)
        for i in range(self.submissions.len()):
            self.submissions.at(i).update(game_time.frame_time)

        if self.people.len() > MAX_PEOPLE:
            return False, self.score

        return self.update_game_timer(game_time)

    def update_game_timer(self, game_time: pyasge.GameTime) -> (bool, int):
        self.timer = self.timer - game_time.fixed_timestep
        self.timer_clock.string = str("{:.1f}".format(self.timer))
        if self.timer < 0:
            return False, self.score
        elif self.timer < 10:
            self.timer_clock.colour = pyasge.COLOURS.YELLOW
        return True, self.score

    def update_spawn_timer(self, game_time: pyasge.GameTime) -> None:
        self.spawn_timer -= game_time.frame_time
        if self.spawn_timer <= 0 and self.people.len() < MAX_PEOPLE + 1:

            # add a new person
            self.total_people += 1
            self.people.enqueue(
                Person(self.total_people, (self.game_data.game_res[0] - X_MARGIN) - (PEOPLE_MARGIN * self.people.len()),
                       40))

            # reset the spawn timer
            self.spawn_timer = random.randint(1, self.people_add)

    def render(self, game_time: pyasge.GameTime) -> None:
        self.game_data.renderer.render(self.desk)
        self.render_queue()  # queue of people

        for i in range(self.submissions.len()):
            self.submissions.at(i).render(self.game_data.renderer)
        if self.submission is not None:
            self.submission.render(self.game_data.renderer)

        for tray in self.submission_trays:
            tray.render(self.game_data.renderer)
        self.next_btn.render(self.game_data.renderer)

        for mode in self.submission_modes:
            self.game_data.renderer.render(mode)

        # render the UI elements last
        self.game_data.renderer.render(self.scoreboard)
        self.game_data.renderer.render(self.timer_clock)
        self.game_data.renderer.render(self.designation)

        if self.people.len() > MAX_PEOPLE - 6:
            self.render_warning(game_time)

    def render_queue(self) -> None:
        for person in range(self.people.len()):
            self.people.at(person).render(self.game_data.renderer)

        if self.active_person is not None:
            self.active_person.render(self.game_data.renderer)

    def render_warning(self, game_time: pyasge.GameTime) -> None:
        if self.warning_fade_mode:
            self.warning.opacity -= 0.155 * game_time.frame_time * self.people.len()
            if self.warning.opacity <= 0:
                self.warning_fade_mode = 0
        else:
            self.warning.opacity += 0.155 * game_time.frame_time * self.people.len()
            if self.warning.opacity >= 1:
                self.warning_fade_mode = 1
        self.game_data.renderer.render(self.warning)
