from lib.rgb import rgb
from lib.svg import SVG, Line, Outline

red = rgb(255, 0, 0)
outer = Outline(red, 2)

l = Line((5, 5), (55, 25), outer)

svg = SVG(60, 30).setData([l])

svgString = svg.export()


def getLine():
    return svgString
