from xmlGen import Declaration, Tag


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
        d = Declaration([("version", "1.0"), ("encoding", "UTF-8")])
        return f"{d}\n{self}"