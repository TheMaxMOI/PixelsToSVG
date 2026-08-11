from ..svgElementClass import SvgElement


class Line(SvgElement):
    def __init__(self, pos1, pos2, outer=None):
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

        super().__init__("line", attributes, None, outer, isEmpty=True)
