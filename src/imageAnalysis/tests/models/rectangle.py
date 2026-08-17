from lib.rgb import rgb
from lib.svg import SVG, Coloring, Outline, Rectangle

red = rgb(255, 0, 0)
inner = Coloring(red)
outer = Outline(red, 2)

r = Rectangle(50, 20, (5, 5), inner, outer)

svg = SVG(60, 30).setData([r])

svgString = svg.export()


def getRectangle():
    return svgString
