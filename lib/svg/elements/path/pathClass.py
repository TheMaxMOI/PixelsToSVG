from ..svgElementClass import SvgElement


class Path(SvgElement):
    isEmpty = True
    name = "path"

    def __init__(self, d, outer=None):
        attributes = [("d", d)]

        super().__init__(Path.name, attributes, None, outer, isEmpty=Path.isEmpty)
