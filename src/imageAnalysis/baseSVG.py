from lib.rgb import rgb
from lib.svg import SVG, Coloring, Rectangle

from .detectShape import findArea, findOutline, findPolygon, smoothPolygon
from .majorColor import findBackground, findPrimary
from .shapingRoughly import getfittestShape


def getBaseSVG(img, background: bool = False, smoothed: bool = False):
    color = findPrimary(img)
    outline = findOutline(findArea(img, color))
    points = findPolygon(outline)

    if smoothed:
        points = smoothPolygon(points)

    shapes = []
    shapes.append(getfittestShape(points, rgb(color[0], color[1], color[2])))
    if background:
        backColor = findBackground(img, color)
        rect = Rectangle(
            img.shape[1],
            img.shape[0],
            inner=Coloring(rgb(backColor[0], backColor[1], backColor[2])),
        )
        shapes.insert(0, rect)

    return SVG(img.shape[1], img.shape[0]).setData(shapes)
