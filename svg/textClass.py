from xmlGen import Tag, getAttrValue

from .utils.shapeUtils import update


class Text(Tag):
    # Careful: set the corner low enough so the text appears
    def __init__(self, bottomLeftPos=(0, 0), additionalAttributes=None):
        self.x = bottomLeftPos[0]
        self.y = bottomLeftPos[1]

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [("x", f"{self.x}"), ("y", f"{self.y}")]

        super().__init__("text", attributes, False)

        self.rot = int(getAttrValue("rotate", self.attributes) or 0)

    def rotate(self, degree):
        self.rot += degree
        self.rot %= 360

        update("rotate", f"{self.rot}", self.attributes)


class Tspan(Text):
    def __init__(self, bottomLeftPos=(0, 0), additionalAttributes=None):
        self.x = bottomLeftPos[0]
        self.y = bottomLeftPos[1]

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [("x", f"{self.x}"), ("y", f"{self.y}")]

        Tag.__init__(self, "tspan", attributes, False)

        self.rot = int(getAttrValue("rotate", self.attributes) or 0)
