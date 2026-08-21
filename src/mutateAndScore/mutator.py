import random
from enum import Enum

from lib.rgb import rgb
from lib.svg import SVG, Circle, Coloring, Outline, Polygon, Rectangle
from lib.svg.elements.utils.mathHelpers import randint

from ..randomize.randomSVG import getRandShape


class Mutation(Enum):
    GEOMETRY = 0.40
    APPEARANCE = 0.30
    SWAP_LAYER = 0.15
    ADD = 0.10
    REMOVE = 0.05


def choose_mutation():
    r = random.random()

    if r < 0.40:
        return 0
    if r < 0.70:
        return 1
    if r < 0.85:
        return 2
    if r < 0.95:
        return 3
    return 4


class Mutator:
    __slots__ = ("elms", "height", "svg", "width")

    def __init__(self, svg: SVG, height, width):
        self.svg = svg
        self.elms = svg.data
        self.height = height
        self.width = width

        self.mutate()

    def get(self):
        self.svg.setData(self.elms)
        return self.svg

    def mutate(self):
        elms = self.elms

        if not elms:
            self.addShape()
            return

        strategy = choose_mutation()
        n = len(elms)

        if strategy == 0:
            self.alterGeometry()
        elif strategy == 1:
            self.alterAppearance()
        elif strategy == 2:
            if n >= 2:
                self.swapLayer()
            else:
                self.alterGeometry()
        elif strategy == 3:
            self.addShape()
        elif n > 1:
            self.removeShape()
        else:
            self.alterGeometry()

    def swapLayer(self):
        elms = self.elms
        n = len(elms)

        i = random.randrange(n)
        j = random.randrange(n - 1)

        if j >= i:
            j += 1

        elms[i], elms[j] = elms[j], elms[i]

    def alterGeometry(self):
        elm = random.choice(self.elms)

        dx, dy = random.randint(-5, 5), random.randint(-5, 5)
        if isinstance(elm, Polygon):
            positions = elm.positions
            i = random.randrange(len(positions))
            x, y = positions[i]

            elm.updatePoint((x + dx, y + dy), i)

        elif isinstance(elm, Circle):
            elm.changeCenter(elm.cx + dx, elm.cy + dy)

        elif isinstance(elm, Rectangle):
            elm.changeTopLeftCorner(elm.x + dx, elm.y + dy)

    def addShape(self):
        self.elms.append(getRandShape().generate(self.height, self.width))

    def alterAppearance(self):
        elm = random.choice(self.elms)

        r, g, b = randint(255, len=3)

        if random.getrandbits(1):
            inner = elm.inner
            baseOpacity = inner.opacity if inner is not None else 0

            opacity = baseOpacity + random.uniform(-0.1, 0.1)
            opacity = max(0.05, min(1.0, opacity))

            elm.updateColoring(Coloring(fill=rgb(r, g, b), opacity=round(opacity, 2)))

        else:
            outer = elm.outer

            if outer is None:
                baseOpacity = 0
                baseWidth = 0
            else:
                baseOpacity = outer.opacity
                baseWidth = outer.width

            opacity = baseOpacity + random.uniform(-0.1, 0.1)
            opacity = max(0.05, min(1.0, opacity))

            width = max(0.5, baseWidth + random.uniform(-0.5, 0.5))

            elm.updateOutline(
                Outline(
                    stroke=rgb(r, g, b),
                    width=round(width, 2),
                    opacity=round(opacity, 2),
                )
            )

    def removeShape(self):
        self.elms.pop(random.randrange(len(self.elms)))
