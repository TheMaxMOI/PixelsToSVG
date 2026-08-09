from svg import SVG, Path, Turtle
from xmlGen import Declaration

d = Declaration([("version", "1.0"), ("encoding", "UTF-8")])

attrs = [("stroke", "#ff0000"), ("stroke-width", "1")]
length = 20
angle = 60

t = Turtle(11, 0, 120)
t.switchPen()
for _ in range(6):
    t.move(length)
    t.rotate(-angle)

curve = t.terminate()
shape = Path(curve, attrs)

svg = SVG(420, 370, [("viewBox", "0 -1 43 37"), ("fill-opacity", "0")]).setData([shape])

print(d)
print(svg)
