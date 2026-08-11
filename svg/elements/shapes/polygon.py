from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update
from ..utils.format import stringify


class Polygon(SvgElement):
    def __init__(self, positions, inner=None, outer=None):
        self.points = positions

        attributes = [("points", stringify(self.points))]

        super().__init__("polygon", attributes, inner, outer, isEmpty=True)

    def popPoint(self):
        self.points.pop()

        update("points", stringify(self.points), self.attributes)

    def addPoint(self, pos):
        self.points.append(pos)

        update("points", stringify(self.points), self.attributes)
