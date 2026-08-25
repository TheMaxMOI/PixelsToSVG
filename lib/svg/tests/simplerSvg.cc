#include "../svg.hh"
#include "../elements/appearance.hh"
#include "../elements/path/path.hh"
#include "../elements/path/cursor.hh"
#include "../elements/shapes/rectangle.hh"

#include <algorithm>
#include <iostream>

int main(void)
{
    Coloring inner{"#2582fb"};
    Rectangle r{29, 36, {0, 0}, inner};
    r.addAttribute({"transform", "translate(13 8)"});

    Rectangle rbase{14, 14, {0, 0}, inner};
    auto r1 = rbase.copy();
    auto r2 = rbase.copy();
    auto r3 = rbase.copy();
    auto r4 = rbase.copy();
    r1.addAttribute({"transform", "translate(18 39) rotate(-45)"});
    r2.addAttribute({"transform", "translate(7.899 26) rotate(-45)"});
    r3.addAttribute({"transform", "translate(26.899 26) rotate(-45)"});
    r4.addAttribute({"transform", "translate(18 13) rotate(-45)"});

    Tag g_bottom{"g", {{"id", "bottom"}}};
    Tag g_left{"g", {{"id", "left"}}};
    Tag g_right{"g", {{"id", "right"}}};
    Tag g_top{"g", {{"id", "top"}}};
    g_bottom.setData({r1});
    g_left.setData({r2});
    g_right.setData({r3});
    g_top.setData({r4});

    Cursor c{13.968, 15.17};
    c.ellipticalArcTo(2.7, 2.7, 0.0, 0.0, 1.0, 11.541, 13.92);
    c.ellipticalArcTo(6.713, 6.713, 0.0, 0.0, 1.0, 10.728, 10.276);
    c.ellipticalArcTo(7.215, 7.215, 0.0, 0.0, 1.0, 11.596, 6.3759999999999994);
    c.ellipticalArcTo(2.784, 2.784, 0.0, 0.0, 1.0, 14.077, 5.0329999999999995);
    c.ellipticalArcTo(2.684, 2.684, 0.0, 0.0, 1.0, 16.545, 6.283999999999999);
    c.ellipticalArcTo(7.283, 7.283, 0.0, 0.0, 1.0, 17.317, 10.043999999999999);
    c.ellipticalArcTo(6.981, 6.981, 0.0, 0.0, 1.0, 16.456, 13.843999999999998);
    c.ellipticalArcTo(2.79, 2.79, 0.0, 0.0, 1.0, 13.968, 15.171);
    c.stopHere();
    c.moveTo(14.05, 6.3);
    c.ellipticalArcTo(1.365, 1.365, 0.0, 0.0, 0.0, 12.761000000000001, 7.281);
    c.ellipticalArcTo(7.967, 7.967, 0.0, 0.0, 0.0, 12.347000000000001, 10.224);
    c.ellipticalArcTo(7.039, 7.039, 0.0, 0.0, 0.0, 12.761000000000001, 12.982);
    c.ellipticalArcTo(1.345, 1.345, 0.0, 0.0, 0.0, 14.029000000000002, 13.901);
    c.ellipticalArcTo(1.323, 1.323, 0.0, 0.0, 0.0, 15.297000000000002, 12.961);
    c.ellipticalArcTo(7.716, 7.716, 0.0, 0.0, 0.0, 15.690000000000003, 10.134);
    c.ellipticalArcTo(7.991, 7.991, 0.0, 0.0, 0.0, 15.3, 7.258);
    c.ellipticalArcTo(1.315, 1.315, 0.0, 0.0, 0.0, 14.05, 6.3);
    c.stopHere();

    Path path{c.toPath(), Coloring{"#fff"}};

    SVG svg{53, 52, {{"viewBox", "0 0 53 52"}, {"version", "1.1"}}};
    svg.setData({r, g_bottom, g_left, g_right, g_top, path});

    std::cout << svg << "\n";
}