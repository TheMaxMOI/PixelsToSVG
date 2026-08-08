from enum import Enum

from xmlGen import Tag

from .utils.mathUtils import Rounder, cos, dist2, distInf, sin


class Boolean:
    def __init__(self, val):
        self.val = 1 if (val) else 0

    def __repr__(self):
        return str(self.val)


class Cursor:
    def moveTo(self, x, y):
        self.x = x
        self.y = y
        self.history.append(f"M{x:.3f},{y:.3f}")
        self.edit = True

        return self

    def __init__(self, x, y):
        self.x = 0
        self.y = 0
        self.edit = None
        self.history = []

        self.moveTo(x, y)

    def lineTo(self, x, y):
        if not self.edit:
            return self

        self.x = x
        self.y = y
        self.history.append(f"L{x:.3f},{y:.3f}")

        return self

    def horizontalTo(self, x):
        if not self.edit:
            return self

        self.x = x
        self.history.append(f"H{x:.3f}")

        return self

    def verticalTo(self, y):
        if not self.edit:
            return self

        self.y = y
        self.history.append(f"V{y:.3f}")

        return self

    def quadraticTo(self, cx, cy, x, y):
        if not self.edit:
            return self

        self.x = x
        self.y = y
        self.history.append(f"Q{cx:.3f},{cy:.3f},{x:.3f},{y:.3f}")

        return self

    def cubicTo(self, cx1, cy1, cx2, cy2, x, y):
        if not self.edit:
            return self

        self.x = x
        self.y = y
        self.history.append(f"C{cx1:.3f},{cy1:.3f},{cx2:.3f},{cy2:.3f},{x:.3f},{y:.3f}")

        return self

    def smoothQuadraticTo(self, x, y):
        if not self.edit:
            return self

        self.x = x
        self.y = y
        self.history.append(f"T{x:.3f},{y:.3f}")

        return self

    def smoothCubicTo(self, cx, cy, x, y):
        if not self.edit:
            return self

        self.x = x
        self.y = y
        self.history.append(f"S{cx:.3f},{cy:.3f},{x:.3f},{y:.3f}")

        return self

    def ellipticalArcTo(self, r1, r2, rot, flip, sweep, x, y):
        if not self.edit:
            return self

        self.x = x
        self.y = y
        self.history.append(
            f"A{r1:.3f},{r2:.3f},{rot:.3f},{Boolean(flip)},{Boolean(sweep)},{x:.3f},{y:.3f}"
        )

        return self

    def stopHere(self):
        if not self.edit:
            return self

        self.edit = False
        self.history.append("Z")

        return self

    def toPath(self):
        if not self.edit:
            self.stopHere()

        return " ".join(self.history)


class Turtle:
    class Pen(Enum):
        UP = False # Not Writing
        DOWN = True # Writing

    class Side(Enum):
        LEFT = False
        RIGHT = True

    class Curve(Enum):
        QUADRATIC = 0
        CUBIC = 1
        SMOOTH_Q = 2
        SMOOTH_C = 3
        ARC = 4

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.angle = 0
        self.pen = self.Pen.UP
        self.cursor = Cursor(x, y)
        self.round = Rounder()

    def switchPen(self):
        self.pen = not self.pen

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 360

    def goto(self, x, y):
        if self.pen == self.Pen.UP:
            self.cursor.moveTo(x, y)
        elif self.pen == self.Pen.DOWN:
            if self.x == x:
                self.cursor.verticalTo(y)
            elif self.y == y:
                self.cursor.horizontalTo(x)
            else:
                self.cursor.lineTo(x, y)

        self.x = self.cursor.x
        self.y = self.cursor.y

    def move(self, d):
        dx, dy = self.round(d * cos(self.angle), d * sin(self.angle))
        self.goto(self.x + dx, self.y + dy)

    def sidewaysOffset(self, distance, side):
        """Vector of length `distance`, normal to current direction.

        LEFT bows the curve to the turtle's left, RIGHT to its right.
        Used to bulge a curve's control point(s) away from the straight
        line between start and end.
        """
        direction = -1 if side == self.Side.RIGHT else 1
        offsetX = direction * -sin(self.angle) * distance
        offsetY = direction * cos(self.angle) * distance

        return offsetX, offsetY

    def forwardOffset(self, distance):
        """Vector of length `distance`, parallel to current direction.

        Used to pull a cubic curve's control points out from the start/end
        points in the direction the turtle is already facing, so the curve
        leaves and arrives tangent to that heading.
        """
        offsetX = cos(self.angle) * distance
        offsetY = sin(self.angle) * distance

        return offsetX, offsetY

    def curveTo(self, x, y, side: Side = Side.LEFT, type: Curve = Curve.QUADRATIC):
        if self.pen == self.Pen.UP:
            self.goto(x, y)
            return

        if type < self.Curve.ARC:
            distance = dist2((x, y), (self.x, self.y))
        else:
            radius = distInf((x, y), (self.x, self.y))

        if type == self.Curve.QUADRATIC:
            distance /= 2

            offsetX, offsetY = self.sidewaysOffset(distance, side)

            controlX = self.x + (x - self.x) / 2 + offsetX
            controlY = self.y + (y - self.y) / 2 + offsetY

            self.cursor.quadraticTo(controlX, controlY, x, y)

        elif type == self.Curve.CUBIC:
            distance /= 3

            normalX, normalY = self.sidewaysOffset(distance, side)
            forwardX, forwardY = self.forwardOffset(distance)

            control1X = self.x + forwardX + normalX
            control1Y = self.y + forwardY + normalY
            control2X = x - forwardX + normalX
            control2Y = y - forwardY + normalY

            self.cursor.cubicTo(control1X, control1Y, control2X, control2Y, x, y)

        elif type == self.Curve.SMOOTH_Q:
            self.cursor.smoothQuadraticTo(x, y)

        elif type == self.Curve.SMOOTH_C:
            distance /= 3

            normalX, normalY = self.sidewaysOffset(distance, side)
            forwardX, forwardY = self.forwardOffset(distance)

            controlX = x - forwardX + normalX
            controlY = y - forwardY + normalY

            self.cursor.smoothCubicTo(controlX, controlY, x, y)

        elif type == self.Curve.ARC:
            radius /= 2
            sweep = side == self.Side.RIGHT

            self.cursor.ellipticalArcTo(radius, radius, 0, False, sweep, x, y)

        self.x = self.cursor.x
        self.y = self.cursor.y

    def terminate(self):
        self.cursor.stopHere()
        return self.cursor.toPath()

class Path(Tag):
    def __init__(self, d, additionalAttributes=None):
        attributes = additionalAttributes if (additionalAttributes) else []
        attributes.append(("d", d))

        super().__init__("path", attributes, True)