from lib.rgb import rgb
from lib.svg import SVG, Circle, Coloring, Outline

red = rgb(255, 0, 0)
inner = Coloring(red)
outer = Outline(red, 2)

c = Circle(10, (15, 15), inner, outer)

svg = SVG(30, 30).setData([c])

svgString = svg.export()


def getCircle():
    return svgString