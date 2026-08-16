from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update
from ..utils.format import stringify


class Polygon(SvgElement):
    def __init__(
        self, positions: list[tuple[int | str, int | str]], inner=None, outer=None
    ):
        self.points = positions

        attributes = [("points", stringify(self.points))]

        super().__init__("polygon", attributes, inner, outer, isEmpty=True)

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
