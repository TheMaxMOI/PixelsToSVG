from xmlGen import Tag, getAttrValue

from .utils.shapeUtils import update


class Rectangle(Tag):
    def __init__(self, width, height, topLeftPos=(0, 0), additionalAttributes=None):
        self.width = width
        self.height = height
        self.x = topLeftPos[0]
        self.y = topLeftPos[1]

        attributes = additionalAttributes if (additionalAttributes) else []
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


class Circle(Tag):
    def __init__(self, radius, center=(0, 0), additionalAttributes=None):
        self.r = radius
        self.x = center[0]
        self.y = center[1]

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [
            ("r", f"{self.r}"),
            ("cx", f"{self.x}"),
            ("cy", f"{self.y}"),
        ]

        super().__init__("circle", attributes, True)

    def changeCenter(self, x, y):
        update("cx", f"{x}", self.attributes)
        update("cy", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)


class Ellipse(Tag):
    def __init__(self, rX, rY, center=(0, 0), additionalAttributes=None):
        self.r = rX
        self.r = rY
        self.x = center[0]
        self.y = center[1]

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [
            ("r", f"{self.rX}"),
            ("r", f"{self.rY}"),
            ("cx", f"{self.x}"),
            ("cy", f"{self.y}"),
        ]

        super().__init__("ellipse", attributes, True)

    def changeCenter(self, x, y):
        update("cx", f"{x}", self.attributes)
        update("cy", f"{y}", self.attributes)

        self.x = int(x)
        self.y = int(y)


class Line(Tag):
    def __init__(self, pos1, pos2, additionalAttributes=None):
        self.x1 = pos1[0]
        self.y1 = pos1[1]
        self.x2 = pos2[0]
        self.y2 = pos2[1]

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes += [
            ("x1", f"{self.x1}"),
            ("y1", f"{self.y1}"),
            ("x2", f"{self.x2}"),
            ("y2", f"{self.y2}"),
        ]

        super().__init__("line", attributes, True)


def stringify(points):
    s = ""

    isFirst = True
    for x, y in points:
        s = f"{s}{'' if isFirst else ' '}{x},{y}"
        isFirst = False

    return s


class Polygon(Tag):
    def __init__(self, positions, additionalAttributes=None):
        self.points = positions

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes.append(("points", stringify(self.points)))

        super().__init__("polygon", attributes, True)

    def popPoint(self):
        self.points.pop()

        update("points", stringify(self.points), self.attributes)

    def addPoint(self, pos):
        self.points.append(pos)

        update("points", stringify(self.points), self.attributes)


class Polyline(Tag):
    def __init__(self, positions, additionalAttributes=None):
        self.points = positions

        attributes = additionalAttributes if (additionalAttributes) else []
        attributes.append(("points", stringify(self.points)))

        super().__init__("polyline", attributes, True)

    def popPoint(self):
        self.points.pop()

        update("points", stringify(self.points), self.attributes)

    def addPoint(self, pos):
        self.points.append(pos)

        update("points", stringify(self.points), self.attributes)
