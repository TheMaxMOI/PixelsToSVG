from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update


class Ellipse(SvgElement):
    def __init__(self, rX, rY, center=(0, 0), inner=None, outer=None):
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

        super().__init__("ellipse", attributes, inner, outer, isEmpty=True)

    def changeCenter(self, x, y):
        update("cx", f"{x}", self.attributes)
        update("cy", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)
