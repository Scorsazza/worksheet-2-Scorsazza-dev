import pyasge
from typing import Tuple

from game.gamedata import GameData


class UserInputWidget:
    done = False        # User has completed entry
    font = None         # The font used to render the characters
    game_data = None    # The shared game data
    char_list = []      # The characters to select from
    name = None         # The player's name
    name_label = None   # The label used to show the name
    selected_idx = 5    # The default selected character

    def __init__(self, shared_data: GameData):
        self.game_data = shared_data

        # Setup the font used
        font_size = 82
        self.font = self.game_data.renderer.loadFont("./data/fonts/arcadeclassic.regular.ttf", font_size)

        # Initialise the char array for selecting letters
        self.init_chars(font_size)

        # Initialise the name label and adjoining name text
        self.init_name_label()

    def init_name_label(self) -> None:
        self.name_label = pyasge.Text(self.font, "NAME")
        self.name_label.colour = pyasge.COLOURS.AQUA
        self.name_label.x = self.char_list[0].x
        self.name_label.y = 800
        self.name = pyasge.Text(self.font)
        self.name.x = self.name_label.x + 250
        self.name.y = self.name_label.y

    def init_chars(self, font_size: int) -> None:
        for n in range(26):
            self.char_list.append(pyasge.Text(self.font, str(chr(pyasge.KEYS.KEY_A + n))))
            self.char_list[-1].x = 400 + (250 * (int(n % 4)))
            self.char_list[-1].y = 125 + font_size * (int(n / 4))

        self.char_list.append(pyasge.Text(self.font, "DEL"))
        self.char_list[-1].x = self.char_list[-2].x + font_size * 3
        self.char_list[-1].y = self.char_list[-2].y

        self.char_list.append(pyasge.Text(self.font, "END"))
        self.char_list[-1].x = self.char_list[-2].x + font_size * 3
        self.char_list[-1].y = self.char_list[-2].y
        self.char_list[self.selected_idx].colour = pyasge.COLOURS.HOTPINK

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_RIGHT:
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.WHITE
                self.selected_idx += 1
                self.selected_idx = max(0, min(self.selected_idx, len(self.char_list) - 1))
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.HOTPINK

            elif event.key == pyasge.KEYS.KEY_LEFT:
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.WHITE
                self.selected_idx -= 1
                self.selected_idx = max(0, min(self.selected_idx, len(self.char_list) - 1))
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.HOTPINK

            elif event.key == pyasge.KEYS.KEY_UP:
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.WHITE
                self.selected_idx -= 4 if self.selected_idx - 4 >= 0 else 0
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.HOTPINK

            elif event.key == pyasge.KEYS.KEY_DOWN:
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.WHITE
                self.selected_idx += 4 if self.selected_idx + 4 < len(self.char_list) else 0
                self.char_list[self.selected_idx].colour = pyasge.COLOURS.HOTPINK

            elif event.key == pyasge.KEYS.KEY_ENTER:
                self.handle_enter_key()

    def handle_enter_key(self) -> None:
        if self.selected_idx == len(self.char_list) - 1:
            self.done = True
        else:
            if self.selected_idx == len(self.char_list) - 2:
                if self.name.string: self.name.string = self.name.string[:-1]
            else:
                self.name.string += self.char_list[self.selected_idx].string

    def update(self) -> Tuple[bool, str]:
        if self.done:
            return True, self.name.string
        else:
            return False, ""

    def render(self) -> None:
        for idx, char in enumerate(self.char_list):
            self.game_data.renderer.render(char)

        self.game_data.renderer.render(self.name_label)
        self.game_data.renderer.render(self.name)
