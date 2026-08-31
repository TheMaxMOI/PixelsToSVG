import math

import cv2
import numpy as np

from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update
from ..utils.format import stringify
from ..utils.mathHelpers import randint


class Polygon(SvgElement):
    isEmpty = True
    name = "polygon"

    def __init__(self, positions: list[tuple[int, int]], inner=None, outer=None):
        self.points = positions

        attributes = [("points", stringify(self.points))]

        super().__init__(Polygon.name, attributes, inner, outer, isEmpty=Polygon.isEmpty)

    def popPoint(self):
        self.points.pop()

    def addPoint(self, point):
        self.points.append(point)

    def insertPoint(self, point, i):
        self.points.insert(i, point)

    def removePoint(self, i):
        self.points.pop(i)

    def updatePoint(self, point, i):
        if i < 0 or i >= len(self.points):
            raise IndexError(
                "Polygon: updatePoint: Out of range index to update point!"
            )

        self.points[i] = point

    def __repr__(self):
        update("points", stringify(self.points), self.attributes)

        return super().__repr__()

    # @staticmethod
    # def generate(height, width):
    #     X = randint(width, len=N)
    #     Y = randint(height, len=N)

    #     points = zip(X, Y)

    #     attributes = [("points", stringify(points))]

    #     return SvgElement.generate(Polygon.name, attributes, Polygon.isEmpty)

    def strokePad(self):
        return math.ceil(self.outer.width / 2) + 1 if self.outer else 0

    def boundingBox(self):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        pad = self.strokePad()
        return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)

    def paintOnMask(self, mask, filled: bool, origin: tuple[int, int]):
        Ox, Oy = origin
        pts = np.array([(x - Ox, y - Oy) for x, y in self.points], dtype=np.int32)
        pts = pts.reshape((-1, 1, 2))

        if filled:
            cv2.fillPoly(mask, [pts], 255, lineType=cv2.LINE_AA)
        else:
            width = max(1, round(self.outer.width)) if self.outer else 1
            cv2.polylines(
                mask, [pts], isClosed=True, color=255, thickness=width, lineType=cv2.LINE_AA
            )