from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update
from ..utils.format import stringify
from ..utils import randint


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