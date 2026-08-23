from ..svgElementClass import SvgElement
from ..utils.attributeUpdater import update
from ..utils import randint


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

        return SvgElement.generate(Circle.name, attributes, Circle.isEmpty)
