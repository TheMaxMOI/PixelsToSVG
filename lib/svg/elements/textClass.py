from lib.xmlGen import getAttrValue

from .svgElementClass import SvgElement
from .utils.attributeUpdater import update


class Text(SvgElement):
    isEmpty = False
    name = "text"

    # Careful: set the corner low enough so the text appears
    def __init__(self, bottomLeftPos=(0, 0), inner=None, outer=None):
        self.x = bottomLeftPos[0]
        self.y = bottomLeftPos[1]

        attributes = [("x", f"{self.x}"), ("y", f"{self.y}")]

        super().__init__(Text.name, attributes, inner, outer, isEmpty=Text.isEmpty)

        self.rot = int(getAttrValue("rotate", self.attributes) or 0)

    def rotate(self, degree):
        self.rot += degree
        self.rot %= 360

        update("rotate", f"{self.rot}", self.attributes)


class Tspan(Text):
    isEmpty = False
    name = "tspan"

    def __init__(self, bottomLeftPos=(0, 0), inner=None, outer=None):
        self.x = bottomLeftPos[0]
        self.y = bottomLeftPos[1]

        attributes = [("x", f"{self.x}"), ("y", f"{self.y}")]

        SvgElement.__init__(self, Tspan.name, attributes, inner, outer, isEmpty=Tspan.isEmpty)

        self.rot = int(getAttrValue("rotate", self.attributes) or 0)
