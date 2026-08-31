import math

import cv2

from lib.xmlGen import getAttrValue

from ..svgElementClass import SvgElement
from ..appearanceClass import Coloring, Outline
from ..utils.attributeUpdater import update
from ..utils.mathHelpers import randint


class Rectangle(SvgElement):
    isEmpty = True
    name = "rect"

    def __init__(
        self,
        width: int,
        height: int,
        topLeftPos: tuple[int, int] = (0, 0),
        inner=None,
        outer=None,
    ):
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

        super().__init__(
            Rectangle.name, attributes, inner, outer, isEmpty=Rectangle.isEmpty
        )

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

    @staticmethod
    def generate(height, width):
        x, w = randint(width, len=2)
        y, h = randint(height, len=2)

        attributes = [
            ("width", f"{w}"),
            ("height", f"{h}"),
            ("x", f"{x}"),
            ("y", f"{y}"),
        ]

        return Rectangle(w,h,(x,y), Coloring.generate(), Outline.generate())

    def strokePad(self):
        return math.ceil(self.outer.width / 2) + 1 if self.outer else 0

    def boundingBox(self):
        pad = self.strokePad()
        return (
            self.x - pad,
            self.y - pad,
            self.x + self.width + pad,
            self.y + self.height + pad,
        )

    def paintOnMask(self, mask, filled: bool, origin: tuple[int, int]): # Corner Rounding skipped
        Ox, Oy = origin
        topLeft = (self.x - Ox, self.y - Oy)
        bottomRight = (self.x + self.width - Ox, self.y + self.height - Oy)

        if filled:
            cv2.rectangle(mask, topLeft, bottomRight, 255, -1, lineType=cv2.LINE_AA)
        else:
            width = max(1, round(self.outer.width)) if self.outer else 1
            cv2.rectangle(mask, topLeft, bottomRight, 255, width, lineType=cv2.LINE_AA)