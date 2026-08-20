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


mutations = list(Mutation)
weights = [m.value for m in mutations]


class Mutator:
    def __init__(self, svg: SVG, height, width):
        self.svg = svg
        self.elms = self.svg.data
        self.height = height
        self.width = width

        self.mutate()

    def get(self):
        self.svg.setData(self.elms)

        return self.svg

    def mutate(self):
        if not self.elms:
            self.addShape()
            return

        strategy = random.choices(mutations, weights=weights, k=1)[0]

        if strategy == Mutation.SWAP_LAYER and len(self.elms) >= 2:
            self.swapLayer()
        elif strategy == Mutation.GEOMETRY:
            self.alterGeometry()
        elif strategy == Mutation.APPEARANCE:
            self.alterAppearance()
        elif strategy == Mutation.ADD:
            self.addShape()
        elif strategy == Mutation.REMOVE and len(self.elms) > 1:
            self.removeShape()
        else:  # default
            self.alterGeometry()

    def swapLayer(self):
        idx1, idx2 = random.sample(range(len(self.elms)), 2)
        self.elms[idx1], self.elms[idx2] = self.elms[idx2], self.elms[idx1]

    def alterGeometry(self):
        elm = random.choice(self.elms)

        if isinstance(elm, Polygon):
            idx = random.randrange(len(elm.positions))
            newX = elm.positions[idx][0] + random.randint(-5, 5)
            newY = elm.positions[idx][1] + random.randint(-5, 5)
            elm.updatePoint((newX, newY), idx)

        elif isinstance(elm, Circle):
            newX = elm.cx + random.randint(-5, 5)
            newY = elm.cy + random.randint(-5, 5)
            elm.changeCenter(newX, newY)

        elif isinstance(elm, Rectangle):
            newX = elm.x + random.randint(-5, 5)
            newY = elm.y + random.randint(-5, 5)
            elm.changeTopLeftCorner(newX, newY)

    def addShape(self):
        shape = getRandShape().generate(self.height, self.width)
        self.elms.append(shape)

    def alterAppearance(self):
        elm = random.choice(self.elms)

        r, g, b = randint(255, len=3)

        if random.choice([True, False]):  # Coloring
            baseOpacity = 0 if (elm.inner is None) else elm.inner.opacity
            opacity = max(0.05, min(1.0, baseOpacity + random.uniform(-0.1, 0.1)))
            elm.updateColoring(Coloring(fill=rgb(r, g, b), opacity=round(opacity, 2)))
        else:  # Outline
            baseOpacity = 0 if (elm.outer is None) else elm.outer.opacity
            baseWidth = 0 if (elm.outer is None) else elm.outer.width
            opacity = max(0.05, min(1.0, baseOpacity + random.uniform(-0.1, 0.1)))
            width = max(0.5, baseWidth + random.uniform(-0.5, 0.5))

            elm.updateOutline(
                Outline(
                    stroke=rgb(r, g, b),
                    width=round(width, 2),
                    opacity=round(opacity, 2),
                )
            )

    def removeShape(self):
        idx = random.randrange(len(self.elms))
        self.elms.pop(idx)
