import numpy as np
from numpy.random import randint

from lib.svg import (
    SVG,
    Circle,
    Ellipse,
    Line,
    # Polygon,
    # Polyline,
    Rectangle,
)

MIN_HEIGHT = 16
MAX_HEIGHT = 3096
MIN_WIDTH = 16
MAX_WIDTH = 4128

shapes = np.array(
    [
        Circle,
        Ellipse,
        Line,
        # Polygon,
        # Polyline,
        Rectangle,
    ]
)
# PointsBased = [Polyline, Polygon]

# def numArgs(func):
#     return func.__code__.co_argcount

def getShapeConstr(amount=None):
    if amount > 0:
        return shapes[randint(0, len(shapes)-1, amount)]
    else:
        return shapes[randint(0, len(shapes)-1)]


def getSVG(shapeAmount: int):
    h, w = randint(MIN_HEIGHT, MAX_HEIGHT), randint(MIN_WIDTH, MAX_WIDTH)

    data = []
    for constr in getShapeConstr(shapeAmount):
        data.append(constr.generate(h, w))

    svg = SVG(h, w).setData(data)

    return svg

