from svg import SVG, Outline, Path, Turtle

outer = Outline("#ff0000", 1)
length = 20
angle = 60

t = Turtle(11, 0, 120)
t.switchPen()
for _ in range(6):
    t.move(length)
    t.rotate(-angle)

curve = t.terminate()
shape = Path(curve, outer=outer)

svg = SVG(420, 370, [("viewBox", "0 -1 43 37"), ("fill-opacity", "0")]).setData([shape])

print(svg.export())
