import pyasge
from tasks.task3_hashtable import HashTable


class MyASGEGame(pyasge.ASGEGame):

    def __init__(self, settings: pyasge.GameSettings):
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.CORNFLOWER)
        self.hashtable = HashTable(1024)

        # register the key and mouse click handlers for this class
        self.key_id = self.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)

        self.init_fonts()

        self.input = ""
        self.status = ""
        self.statusTimer = 0

    def init_fonts(self) -> None:
        self.font = self.renderer.loadFont("/data/fonts/emulogic.ttf", 52)

    def parseInput(self):
        if '.' in self.input:
            try:
                floats = float(self.input)
                return floats
            except ValueError:
                return self.input
        try:
            ints = int(self.input)
            return ints
        except:
            return self.input

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.key == pyasge.KEYS.KEY_ESCAPE:
            self.signalExit()

        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_ENTER:
                tohash = self.parseInput()
                if self.hashtable.contains(tohash):
                    self.status = "Found"
                    self.statusTimer = 1
                else:
                    self.hashtable.insert(tohash)
                    if self.hashtable.contains_anything():
                        self.status = "Inserted"
                        self.statusTimer = 1
                self.input = ""

            if pyasge.KEYS.KEY_A <= event.key <= pyasge.KEYS.KEY_Z or event.key == pyasge.KEYS.KEY_PERIOD or pyasge.KEYS.KEY_0 <= event.key <= pyasge.KEYS.KEY_9:
                self.input = self.input + chr(event.key)

    def update(self, game_time: pyasge.GameTime) -> None:
        if self.statusTimer > 0:
            self.statusTimer -= game_time.fixed_timestep
            if self.statusTimer < 0:
                self.status = ""
                self.statusTimer = 0

    def render(self, game_time: pyasge.GameTime) -> None:
        enter_text = pyasge.Text(self.font, ">")
        enter_text.colour = pyasge.COLOURS.WHITE
        enter_text.y = 100
        enter_text.x = 10
        self.renderer.render(enter_text)

        input_text = pyasge.Text(self.font, self.input)
        input_text.colour = pyasge.COLOURS.WHITE
        input_text.y = 100
        input_text.x = 100
        self.renderer.render(input_text)

        if len(self.status) > 0:
            status = pyasge.Text(self.font, self.status)
            status.colour = pyasge.COLOURS.GREEN
            status.y = 300
            status.x = 300
            self.renderer.render(status)

