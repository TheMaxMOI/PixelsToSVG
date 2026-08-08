from xmlGen import Tag


class SVG(Tag):
    def __init__(self, width, height, additionalAttributes=None):
        self.width = width
        self.height = height

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [("width", f"{width}"), ("height", f"{height}")]
        super().__init__("svg", attributes, False)
