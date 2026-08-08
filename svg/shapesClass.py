from xmlGen import Tag, getAttrValue


def updateAttribute(attrName, newVal, attributes):
    i = 0
    for key, _ in attributes:
        if key == attrName:
            break
        i += 1

    if i < len(attributes):
        attributes[i] = (attrName, newVal)
        return True

    return False


update = lambda attrName, newVal, attributes: (
    ()
    if updateAttribute(attrName, newVal, attributes)
    else attributes.append((attrName, newVal))
)


class Rectangle(Tag):
    def __init__(self, width, height, topLeftPos=(0, 0), additonalAttributes=None):
        self.width = width
        self.height = height
        self.x = topLeftPos[0]
        self.y = topLeftPos[1]

        attributes = additonalAttributes if (additonalAttributes) else []
        attributes += [
            ("width", f"{self.width}"),
            ("height", f"{self.height}"),
            ("x", f"{self.x}"),
            ("y", f"{self.y}"),
        ]

        super().__init__("rect", attributes, True)

        self.rx = int(getAttrValue("rx")) or 0
        self.ry = int(getAttrValue("ry")) or 0

    def changeTopLeftCorner(self, x, y):
        update("x", f"{x}", self.attributes)
        update("y", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)

    def setCornerXRadius(self, rx):
        update("rx", f"{rx}", self.attributes)

        self.rx = int(rx)

    def setCornerYRadius(self, ry):
        update("ry", f"{ry}", self.attributes)

        self.ry = int(ry)