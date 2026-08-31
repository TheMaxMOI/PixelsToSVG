import math

import cv2

from ..svgElementClass import SvgElement
from ..utils.mathHelpers import randint
from ..appearanceClass import Outline


class Line(SvgElement):
    isEmpty = True
    name = "line"

    def __init__(self, pos1: tuple[int, int], pos2: tuple[int, int], outer=None):
        self.x1 = pos1[0]
        self.y1 = pos1[1]
        self.x2 = pos2[0]
        self.y2 = pos2[1]

        attributes = [
            ("x1", f"{self.x1}"),
            ("y1", f"{self.y1}"),
            ("x2", f"{self.x2}"),
            ("y2", f"{self.y2}"),
        ]

        super().__init__(Line.name, attributes, None, outer, isEmpty=Line.isEmpty)

    @staticmethod
    def generate(height, width):
        x1, x2 = randint(width, len=2)
        y1, y2 = randint(height, len=2)
        attributes = [
            ("x1", f"{x1}"),
            ("y1", f"{y1}"),
            ("x2", f"{x2}"),
            ("y2", f"{y2}"),
        ]

        return Line((x1,y1),(x2,y2), Outline.generate())

    def strokePad(self):
        return math.ceil(self.outer.width / 2) + 1 if self.outer else 0

    def boundingBox(self):
        pad = self.strokePad()
        x0, x1 = sorted((self.x1, self.x2))
        y0, y1 = sorted((self.y1, self.y2))
        return (x0 - pad, y0 - pad, x1 + pad, y1 + pad)

    def paintOnMask(self, mask, filled: bool, origin: tuple[int, int]):
        if filled:
            return

        Ox, Oy = origin
        p1 = (self.x1 - Ox, self.y1 - Oy)
        p2 = (self.x2 - Ox, self.y2 - Oy)
        width = max(1, round(self.outer.width)) if self.outer else 1
        cv2.line(mask, p1, p2, 255, width, lineType=cv2.LINE_AA)