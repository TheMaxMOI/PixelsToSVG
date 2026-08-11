from enum import Enum

from ...utils.mathUtils import Rounder, cos, dist2, distInf, sin
from .cursor import Cursor


class Turtle:
    class Pen(Enum):
        UP = False  # Not Writing
        DOWN = True  # Writing

    class Side(Enum):
        LEFT = False
        RIGHT = True

    class Curve(Enum):
        QUADRATIC = 0
        CUBIC = 1
        SMOOTH_Q = 2
        SMOOTH_C = 3
        ARC = 4

    def __init__(self, x=0, y=0, rot=0, precision=3):
        self.x = x
        self.y = y
        self.angle = rot
        self.pen = self.Pen.UP
        self.cursor = Cursor(x, y)
        self.round = Rounder(precision)

    def switchPen(self):
        self.pen = self.Pen.DOWN if self.pen == self.Pen.UP else self.Pen.UP

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 360

        return self

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

        return self

    def move(self, d):
        dx, dy = self.round(d * cos(self.angle), d * sin(self.angle))
        self.goto(self.x + dx, self.y + dy)

        return self

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
            return self

        if type.value < self.Curve.ARC.value:
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

        return self

    def terminate(self):
        self.cursor.stopHere()
        return self.cursor.toPath()
