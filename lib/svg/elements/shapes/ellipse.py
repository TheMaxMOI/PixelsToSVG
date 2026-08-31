import math

import cv2

from ..svgElementClass import SvgElement
from ..appearanceClass import Coloring, Outline
from ..utils.attributeUpdater import update
from ..utils.mathHelpers import randint


class Ellipse(SvgElement):
    isEmpty = True
    name = "ellipse"

    def __init__(
        self, rX: int, rY: int, center: tuple[int, int] = (0, 0), inner=None, outer=None
    ):
        self.rX = rX
        self.rY = rY
        self.x = center[0]
        self.y = center[1]

        attributes = [
            ("rx", f"{self.rX}"),
            ("ry", f"{self.rY}"),
            ("cx", f"{self.x}"),
            ("cy", f"{self.y}"),
        ]

        super().__init__(
            Ellipse.name, attributes, inner, outer, isEmpty=Ellipse.isEmpty
        )

    def changeCenter(self, x, y):
        update("cx", f"{x}", self.attributes)
        update("cy", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)

    @staticmethod
    def generate(height, width):
        rX, rY = randint(min(height, width), len=2)
        x, y = randint(width), randint(height)

        attributes = [
            ("rx", f"{rX}"),
            ("ry", f"{rY}"),
            ("cx", f"{x}"),
            ("cy", f"{y}"),
        ]

        return Ellipse(rX,rY,(x,y),Coloring.generate(), Outline.generate())

    def strokePad(self):
        return math.ceil(self.outer.width / 2) + 1 if self.outer else 0

    def boundingBox(self):
        pad = self.strokePad()
        return (
            self.x - self.rX - pad,
            self.y - self.rY - pad,
            self.x + self.rX + pad,
            self.y + self.rY + pad,
        )

    def paintOnMask(self, mask, filled: bool, origin: tuple[int, int]):
        Ox, Oy = origin
        center = (self.x - Ox, self.y - Oy)
        axes = (self.rX, self.rY)

        if filled:
            cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1, lineType=cv2.LINE_AA)
        else:
            width = max(1, round(self.outer.width)) if self.outer else 1
            cv2.ellipse(mask, center, axes, 0, 0, 360, 255, width, lineType=cv2.LINE_AA)