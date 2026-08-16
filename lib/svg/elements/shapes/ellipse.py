from ..svgElementClass import SvgElement
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

        return SvgElement.generate(Ellipse.name, attributes, Ellipse.isEmpty)
