from lib.rgb import rgb
from lib.svg import SVG, Circle, Coloring, Outline, Rectangle

red = rgb(255, 0, 0)
inner = Coloring(red)
outer = Outline(red, 2)

c = Circle(10, (15, 15), inner, outer)
back = Rectangle(30, 30, inner=Coloring(rgb(0, 255, 0)))

svg = SVG(30, 30).setData([back, c])

svgString = svg.export()


def getCircle():
    return svgString