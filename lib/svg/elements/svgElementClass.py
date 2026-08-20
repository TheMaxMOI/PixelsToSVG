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
        self.inner = inner
        self.outer = outer

        allAttributes = attributes.copy() if (attributes) else []
        if inner != None:
            allAttributes += inner.use()
        if outer != None:
            allAttributes += outer.use()

        super().__init__(name, allAttributes, isEmpty)

    @staticmethod
    def generate(name, attributes, isEmpty):
        return SvgElement(
            name, attributes, Coloring.generate(), Outline.generate(), isEmpty
        )

    def updateColoring(self, inner: Coloring):
        if self.inner is None:
            self.attributes += inner.use()
        else:
            for name, val in inner.use():
                update(name, val, self.attributes)

        self.inner = inner

    def updateOutline(self, outer: Outline):
        if self.outer is None:
            self.attributes += outer.use()
        else:
            for name, val in outer.use():
                update(name, val, self.attributes)

        self.outer = outer