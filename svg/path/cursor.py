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
