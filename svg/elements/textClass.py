from xmlGen import getAttrValue

from .svgElementClass import SvgElement
from .utils.attributeUpdater import update


class Text(SvgElement):
    # Careful: set the corner low enough so the text appears
    def __init__(self, bottomLeftPos=(0, 0), inner=None, outer=None):
        self.x = bottomLeftPos[0]
        self.y = bottomLeftPos[1]

        attributes = [("x", f"{self.x}"), ("y", f"{self.y}")]

        super().__init__("text", attributes, inner, outer, isEmpty=False)

        self.rot = int(getAttrValue("rotate", self.attributes) or 0)

    def rotate(self, degree):
        self.rot += degree
        self.rot %= 360

        update("rotate", f"{self.rot}", self.attributes)


class Tspan(Text):
    def __init__(self, bottomLeftPos=(0, 0), inner=None, outer=None):
        self.x = bottomLeftPos[0]
        self.y = bottomLeftPos[1]

        attributes = [("x", f"{self.x}"), ("y", f"{self.y}")]

        SvgElement.__init__(self, "tspan", attributes, inner, outer, isEmpty=False)

        self.rot = int(getAttrValue("rotate", self.attributes) or 0)
