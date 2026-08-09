from xmlGen import Declaration, Tag

from .textClass import Text, Tspan


class SVG(Tag):
    def __init__(self, width, height, additionalAttributes=None):
        self.width = width
        self.height = height

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [
            ("width", f"{width}"),
            ("height", f"{height}"),
            ("xmlns", "http://www.w3.org/2000/svg"),
        ]

        super().__init__("svg", attributes, False)

    def export(self):
        if not self.checkTspan():
            raise SyntaxError(
                "Tspan instances must be children of other Tspan or Text instances!"
            )

        d = Declaration([("version", "1.0"), ("encoding", "UTF-8")])
        return f"{d}\n{self}"

    def checkTspan(self):
        def check(tag, parent=None):
            if isinstance(tag, Tspan) and not isinstance(parent, (Text, Tspan)):
                return False

            if tag.data:
                return all(
                    check(child, tag) for child in tag.data if isinstance(child, Tag)
                )

            return True

        return check(self)
