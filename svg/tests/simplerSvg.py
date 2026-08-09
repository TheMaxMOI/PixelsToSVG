from svg import SVG, Cursor, Path, Rectangle
from xmlGen import Declaration, Tag

d = Declaration([("version", "1.0"), ("encoding", "UTF-8")])

r = Rectangle(
    29, 36, additionalAttributes=[("transform", "translate(13 8)"), ("fill", "#2582fb")]
)
rbase = Rectangle(14, 14).addAttribute(("fill", "#2582fb"))
r1 = rbase.copy().addAttribute(("transform", "translate(18 39) rotate(-45)"))
r2 = rbase.copy().addAttribute(("transform", "translate(7.899 26) rotate(-45)"))
r3 = rbase.copy().addAttribute(("transform", "translate(26.899 26) rotate(-45)"))
r4 = rbase.copy().addAttribute(("transform", "translate(18 13) rotate(-45)"))

g_bottom = Tag("g", [("id", "bottom")]).setData([r1])
g_left = Tag("g", [("id", "left")]).setData([r2])
g_right = Tag("g", [("id", "right")]).setData([r3])
g_top = Tag("g", [("id", "top")]).setData([r4])

curve = (
    Cursor(13.968, 15.17)
    .ellipticalArcTo(2.7, 2.7, 0.0, 0.0, 1.0, 11.541, 13.92)
    .ellipticalArcTo(6.713, 6.713, 0.0, 0.0, 1.0, 10.728, 10.276)
    .ellipticalArcTo(7.215, 7.215, 0.0, 0.0, 1.0, 11.596, 6.3759999999999994)
    .ellipticalArcTo(2.784, 2.784, 0.0, 0.0, 1.0, 14.077, 5.0329999999999995)
    .ellipticalArcTo(2.684, 2.684, 0.0, 0.0, 1.0, 16.545, 6.283999999999999)
    .ellipticalArcTo(7.283, 7.283, 0.0, 0.0, 1.0, 17.317, 10.043999999999999)
    .ellipticalArcTo(6.981, 6.981, 0.0, 0.0, 1.0, 16.456, 13.843999999999998)
    .ellipticalArcTo(2.79, 2.79, 0.0, 0.0, 1.0, 13.968, 15.171)
    .stopHere()
    .moveTo(14.05, 6.3)
    .ellipticalArcTo(1.365, 1.365, 0.0, 0.0, 0.0, 12.761000000000001, 7.281)
    .ellipticalArcTo(7.967, 7.967, 0.0, 0.0, 0.0, 12.347000000000001, 10.224)
    .ellipticalArcTo(7.039, 7.039, 0.0, 0.0, 0.0, 12.761000000000001, 12.982)
    .ellipticalArcTo(1.345, 1.345, 0.0, 0.0, 0.0, 14.029000000000002, 13.901)
    .ellipticalArcTo(1.323, 1.323, 0.0, 0.0, 0.0, 15.297000000000002, 12.961)
    .ellipticalArcTo(7.716, 7.716, 0.0, 0.0, 0.0, 15.690000000000003, 10.134)
    .ellipticalArcTo(7.991, 7.991, 0.0, 0.0, 0.0, 15.3, 7.258)
    .ellipticalArcTo(1.315, 1.315, 0.0, 0.0, 0.0, 14.05, 6.3)
    .stopHere()
    .toPath()
)
path = Path(curve, [("transform", "translate(13.5 15.689)"), ("fill", "#fff")])

svg = SVG(53, 52, [("viewBox", "0 0 53 52"), ("version", "1.1")]).setData(
    [r, g_bottom, g_left, g_right, g_top, path]
)

print(d)
print(svg)
