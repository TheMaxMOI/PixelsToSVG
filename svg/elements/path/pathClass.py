from ..svgElementClass import SvgElement


class Path(SvgElement):
    def __init__(self, d, outer=None):
        attributes = [("d", d)]

        super().__init__("path", attributes, None, outer, isEmpty=True)
