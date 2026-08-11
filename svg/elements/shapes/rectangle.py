from xmlGen import getAttrValue

from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update


class Rectangle(SvgElement):
    def __init__(self, width, height, topLeftPos=(0, 0), inner=None, outer=None):
        self.width = width
        self.height = height
        self.x = topLeftPos[0]
        self.y = topLeftPos[1]

        attributes = [
            ("width", f"{self.width}"),
            ("height", f"{self.height}"),
            ("x", f"{self.x}"),
            ("y", f"{self.y}"),
        ]

        super().__init__("rect", attributes, inner, outer, isEmpty=True)

        self.rx = int(getAttrValue("rx", self.attributes) or 0)
        self.ry = int(getAttrValue("ry", self.attributes) or 0)

    def changeTopLeftCorner(self, x, y):
        update("x", f"{x}", self.attributes)
        update("y", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)

    def setCornerXRadius(self, rx):
        update("rx", f"{rx}", self.attributes)

        self.rx = int(rx)

    def setCornerYRadius(self, ry):
        update("ry", f"{ry}", self.attributes)

        self.ry = int(ry)