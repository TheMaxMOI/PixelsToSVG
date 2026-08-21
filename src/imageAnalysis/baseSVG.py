from lib.rgb import rgb
from lib.svg import SVG, Coloring, Rectangle

from .detectShape import findArea, findPolygon, smoothPolygon
from .majorColor import findPrimary, findPrimaryAndBackground
from .shapingRoughly import getfittestShape


def getBaseSVG(img, background: bool = False, smoothed: bool = False):
    if background:
        color, backColor = findPrimaryAndBackground(img)
    else:
        color = findPrimary(img)

    area = findArea(img, color)
    points = findPolygon(area)

    if smoothed:
        points = smoothPolygon(points)

    shapes = []

    if background:
        rect = Rectangle(
            img.shape[1],
            img.shape[0],
            inner=Coloring(rgb(backColor[0], backColor[1], backColor[2])),
        )
        shapes.append(rect)

    shapes.append(getfittestShape(points, rgb(color[0], color[1], color[2])))

    return SVG(img.shape[1], img.shape[0]).setData(shapes)
