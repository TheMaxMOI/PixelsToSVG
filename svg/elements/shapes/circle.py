from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update


class Circle(SvgElement):
    def __init__(self, radius, center=(0, 0), inner=None, outer=None):
        self.r = radius
        self.x = center[0]
        self.y = center[1]

        attributes = [
            ("r", f"{self.r}"),
            ("cx", f"{self.x}"),
            ("cy", f"{self.y}"),
        ]

        super().__init__("circle", attributes, inner, outer, isEmpty=True)

    def changeCenter(self, x, y):
        update("cx", f"{x}", self.attributes)
        update("cy", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)