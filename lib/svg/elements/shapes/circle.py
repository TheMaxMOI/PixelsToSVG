import math

import cv2

from ..svgElementClass import SvgElement
from ..appearanceClass import Coloring, Outline
from ..utils.attributeUpdater import update
from ..utils.mathHelpers import randint


class Circle(SvgElement):
    isEmpty = True
    name = "circle"

    def __init__(
        self, radius: int, center: tuple[int, int] = (0, 0), inner=None, outer=None
    ):
        self.r = radius
        self.x = center[0]
        self.y = center[1]

        attributes = [
            ("r", f"{self.r}"),
            ("cx", f"{self.x}"),
            ("cy", f"{self.y}"),
        ]

        super().__init__(Circle.name, attributes, inner, outer, isEmpty=True)

    def changeCenter(self, x, y):
        update("cx", f"{x}", self.attributes)
        update("cy", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)

    @staticmethod
    def generate(height, width):
        r = randint(min(height, width))
        x, y = randint(width), randint(height)

        attributes = [
            ("r", f"{r}"),
            ("cx", f"{x}"),
            ("cy", f"{y}"),
        ]

        return Circle(r, (x,y), Coloring.generate(), Outline.generate())

    def strokePad(self):
        return math.ceil(self.outer.width / 2) + 1 if self.outer else 0

    def boundingBox(self):
        pad = self.strokePad()
        return (
            self.x - self.r - pad,
            self.y - self.r - pad,
            self.x + self.r + pad,
            self.y + self.r + pad,
        )

    def paintOnMask(self, mask, filled: bool, origin: tuple[int, int]):
        Ox, Oy = origin
        center = (self.x - Ox, self.y - Oy)

        if filled:
            cv2.circle(mask, center, self.r, 255, -1, lineType=cv2.LINE_AA)
        else:
            width = max(1, round(self.outer.width)) if self.outer else 1
            cv2.circle(mask, center, self.r, 255, width, lineType=cv2.LINE_AA)