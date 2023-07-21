import pyasge

from tasks.task4_quadtree import QuadTreeNode


class MyASGEGame(pyasge.ASGEGame):

    def __init__(self, settings: pyasge.GameSettings):
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.CORNFLOWER)

        # register the key and mouse click handlers for this class
        self.key_id = self.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)
        self.mouse_id = self.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_handler)

        # Create the root node of the quad tree
        self.node = QuadTreeNode(pyasge.Point2D(0, 0), pyasge.Point2D(settings.window_width, settings.window_height))

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.action == 1 and event.button == 0:
            sprite = pyasge.Sprite()
            sprite.loadTexture(f"./data/quadtree/Sprite.png")
            sprite.x = event.x - int(sprite.width / 2)
            sprite.y = event.y - int(sprite.height / 2)
            sprite.z_order = 0
            self.node.add(sprite)
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.key == pyasge.KEYS.KEY_ESCAPE:
            self.signalExit()

    def update(self, game_time: pyasge.GameTime) -> None:
        pass

    def render(self, game_time: pyasge.GameTime) -> None:
        self.node.render_recursively(self.renderer)
        pass
