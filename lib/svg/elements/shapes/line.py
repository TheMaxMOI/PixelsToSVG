from ..svgElementClass import SvgElement
from ..utils.mathHelpers import randint


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

        return super().generate(Line.name, attributes, Line.isEmpty)