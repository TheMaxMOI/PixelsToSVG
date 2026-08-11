from xmlGen import Tag


class Path(Tag):
    def __init__(self, d, additionalAttributes=None):
        attributes = additionalAttributes if (additionalAttributes) else []
        attributes.append(("d", d))

        super().__init__("path", attributes, True)
