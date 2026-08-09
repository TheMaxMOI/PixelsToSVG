from svg import SVG, Line

attrs = [("stroke", "#ff0000"), ("stroke-width", "1")]
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

l1 = Line(vertices[0], vertices[1], attrs.copy())
l2 = Line(vertices[1], vertices[2], attrs.copy())
l3 = Line(vertices[2], vertices[3], attrs.copy())
l4 = Line(vertices[3], vertices[4], attrs.copy())
l5 = Line(vertices[4], vertices[5], attrs.copy())
l6 = Line(vertices[5], vertices[0], attrs.copy())

svg = SVG(420, 370, [("viewBox", "-1 -1 42 37")]).setData([l1, l2, l3, l4, l5, l6])

print(svg.export())
