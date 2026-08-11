from xmlGen import Tag

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
            allAttributes += inner.use()

        super().__init__(name, allAttributes, isEmpty)
