from svg import SVG, Outline, Path, Turtle

outer = Outline("#ff0000", 1)
sqrt3 = round(3**0.5, ndigits=3)
vertices = [
    (1.5, sqrt3),
    (0.5, sqrt3),
    (0, sqrt3 / 2),
    (0.5, 0),
    (1.5, 0),
    (2, sqrt3 / 2),
]
scale = 20
vertices = [(scale * x, scale * y) for x, y in vertices]

path = vertices + [vertices[0]]

t = Turtle()
isFirst = True
for x, y in path:
    if isFirst:
        isFirst = False
        t.goto(x, y)
        t.switchPen()
    else:
        t.curveTo(x, y, type=Turtle.Curve.ARC)

curve = t.terminate()
shape = Path(curve, outer=outer)

svg = SVG(420, 370, [("viewBox", "-1 -1 42 37"), ("fill-opacity", "0")]).setData(
    [shape]
)

print(svg.export())
