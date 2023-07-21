import pyasge


class QuadTreeNode:
    def __init__(self, _min=pyasge.Point2D(0, 0), _max=pyasge.Point2D(1.0, 1.0)):
        self.bounds_max = _max  # This stores the maximum of the node, and we are using the pyasge Point2D class to store this
        self.bounds_min = _min  # Likewise for the minimum
        self.children = []  # List of children, should be zero or four
        self.data = []  # List of Sprites stored in this node
        self.borders = []  # Sprites used to draw the borders
        self.borders.append(self.add_border(self.bounds_min.x, self.bounds_min.y, self.bounds_max.x - self.bounds_min.x,
                                            1))  # These lines simply create the border lines
        self.borders.append(
            self.add_border(self.bounds_min.x, self.bounds_max.y - 1, self.bounds_max.x - self.bounds_min.x, 1))
        self.borders.append(
            self.add_border(self.bounds_min.x, self.bounds_min.y, 1, self.bounds_max.y - self.bounds_min.y))
        self.borders.append(
            self.add_border(self.bounds_max.x - 1, self.bounds_min.y, 1, self.bounds_max.y - self.bounds_min.y))

    def add_border(self, x, y, w, h):  # This creates a border sprite
        border = pyasge.Sprite()
        border.loadTexture(f"./data/quadtree/border.png")
        border.x = x
        border.y = y
        border.width = w
        border.height = h
        return border

    def add(self, sprite):  # This is the method to add recursive addition of data to the quad tree
        # This is where you need to add your code. We have provided comments to say what each step of the code should do
        # First, we need to check if this node is a leaf or not (hint use the method isLeaf()
        # If it is an interior node then we need to:
        #    Iterate through each child
        #        Find if the centre x and y coordinates of the sprite are inside the child node (hint call the inside method on the child node)
        #        If they are, add the sprite to the child node and return
        # If it is a leaf node
        #    If there is nothing in self.data or if self.canSplit() == False then add the sprite to self.data and return
        #    Otherwise we have to split this node by performing the following steps:
        #        Find the mid point of the current node
        #        Create four child QuadTreeNode which split the quadtrant into four sub quadrants:
        #         -----    -----
        #        |    |    | | |
        #        |    | -> -----
        #        |    |    | | |
        #         -----    -----
        #        Add these QuadTreeNode to self.children
        #        Then we need to add the contents of self.data to the appropriate child nodes like we did above
        #        And we also need to add sprite to the appropriate child nodes like we did above with centre x and y coordinates
        #        Finally, we want to clear the contents of self.data as we already have stored this in the child nodes of the current node
        pass

    def inside(self, point: pyasge.Point2D) -> bool:  # Check if a point is inside the quadtree node
        # Add code here to check if the point is between self.bounds_min and self.bounds_max
        return False

    def is_leaf(self):  # Returns true if the node is a leaf
        if len(self.children) > 0:
            return True
        return False

    def can_split(self):  # A heuristic to stop recursion. You may want to check this before splitting a node
        w = self.bounds_max.x - self.bounds_min.x
        h = self.bounds_max.y - self.bounds_min.y
        if (w * h) < 4:
            return False
        return True

    def render_recursively(self, renderer):  # Draws the node and all children recursively
        if len(self.children) > 0:
            for child in self.children:
                child.render_recursively(renderer)
        for border in self.borders:
            renderer.render(border)
        for item in self.data:
            renderer.render(item)
