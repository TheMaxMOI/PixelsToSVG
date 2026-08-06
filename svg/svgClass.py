from xmlGen import Tag, Declaration

class SVG(Tag):
    def __init__(self, width, height, additionalAttributes = None):
        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [("width", f"{width}"), ("height", f"{height}")]
        super().__init__("svg", attributes, False)