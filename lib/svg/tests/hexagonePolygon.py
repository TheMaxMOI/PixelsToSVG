from svg import SVG, Coloring, Outline, Polygon

inner = Coloring("#000000", 0)
outer = Outline("#ff0000", 1, 1)
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

shape = Polygon(vertices, inner=inner, outer=outer)

svg = SVG(420, 370, [("viewBox", "-1 -1 42 37")]).setData([shape])

print(svg.export())
