from svg import SVG, Rectangle
from xmlGen import Declaration, Tag

d = Declaration([("version", "1.0"), ("encoding", "UTF-8")])

r = Rectangle(29, 36, additionalAttributes=[("transform", "translate(13 8)"), ("fill", "#2582fb")])
rbase = Rectangle(14, 14).addAttribute(("fill", "#2582fb"))
r1 = rbase.copy().addAttribute(("transform", "translate(18 39) rotate(-45)"))
r2 = rbase.copy().addAttribute(("transform", "translate(7.899 26) rotate(-45)"))
r3 = rbase.copy().addAttribute(("transform", "translate(26.899 26) rotate(-45)"))
r4 = rbase.copy().addAttribute(("transform", "translate(18 13) rotate(-45)"))

g_bottom = Tag("g", [("id", "bottom")]).setData([r1])
g_left = Tag("g", [("id", "left")]).setData([r2])
g_right = Tag("g", [("id", "right")]).setData([r3])
g_top = Tag("g", [("id", "top")]).setData([r4])

svg = SVG(53, 52, [("viewBox", "0 0 53 52"), ("version", "1.1")]).setData(
    [r, g_bottom, g_left, g_right, g_top]
)

print(d)
print(svg)