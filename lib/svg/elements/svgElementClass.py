from lib.xmlGen import Tag

from .appearanceClass import Coloring, Outline
from .utils.attributeUpdater import update


class SvgElement(Tag):
    def __init__(
        self,
        name: str,
        attributes: list[tuple[str, str]] | None = None,
        inner: Coloring = None,
        outer: Outline = None,
        isEmpty: bool = False,
    ):
        super().__init__(name, attributes.copy() if attributes else [], isEmpty)

        self.inner = None
        self.outer = None

        if inner is not None:
            self.updateColoring(inner)
        if outer is not None:
            self.updateOutline(outer)

    @staticmethod
    def generate(name, attributes, isEmpty):
        return SvgElement(
            name, attributes, Coloring.generate(), Outline.generate(), isEmpty
        )

    def updateColoring(self, inner: Coloring):
        if inner is not None:
            for name, val in inner.use():
                update(name, val, self.attributes)

        self.inner = inner

    def updateOutline(self, outer: Outline):
        if outer is not None:
            for name, val in outer.use():
                update(name, val, self.attributes)

        self.outer = outer
