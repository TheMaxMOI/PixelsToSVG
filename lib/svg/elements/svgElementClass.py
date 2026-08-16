from lib.xmlGen import Tag

from .appearanceClass import Coloring, Outline


class SvgElement(Tag):
    def __init__(
        self,
        name: str,
        attributes: list[tuple[str, str]] | None = None,
        inner: Coloring = None,
        outer: Outline = None,
        isEmpty: bool = False,
    ):
        allAttributes = attributes.copy() if (attributes) else []
        if inner != None:
            allAttributes += inner.use()
        if outer != None:
            allAttributes += outer.use()

        super().__init__(name, allAttributes, isEmpty)

    @staticmethod
    def generate(name, attributes, isEmpty):
        allAttributes = attributes.copy() if (attributes) else []
        allAttributes += Coloring.generate().use() + Outline.generate().use()

        return SvgElement(name, allAttributes, isEmpty)
