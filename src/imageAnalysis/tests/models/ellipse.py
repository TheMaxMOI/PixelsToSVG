from lib.rgb import rgb
from lib.svg import SVG, Coloring, Ellipse, Outline

red = rgb(255, 0, 0)
inner = Coloring(red)
outer = Outline(red, 2)

e = Ellipse(25, 10, (30, 15), inner, outer)

svg = SVG(60, 30).setData([e])

svgString = svg.export()


def getEllipse():
    return svgString
