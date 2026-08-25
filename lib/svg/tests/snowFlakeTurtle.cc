#include "../svg.hh"
#include "../elements/appearance.hh"
#include "../elements/path/path.hh"
#include "../elements/path/turtle.hh"

#include <algorithm>
#include <iostream>

int main(void)
{
    Outline outer{"#ff0000", 1};
    double sqrt3 = 1.732;

    std::vector<std::tuple<double, double>> vertices{
        {1.5, sqrt3},
        {0.5, sqrt3},
        {0, sqrt3 / 2},
        {0.5, 0},
        {1.5, 0},
        {2, sqrt3 / 2}};

    double scale = 20;
    std::transform(vertices.begin(), vertices.end(),
                   vertices.begin(),
                   [scale](const std::tuple<double, double> &p) -> std::tuple<double, double>
                   {
                       return {std::get<0>(p) * scale, std::get<1>(p) * scale};
                   });

    std::vector<std::tuple<double, double>> path = vertices;
    path.push_back(vertices.at(0));

    Turtle t{};
    bool isFirst = true;
    for (auto [x, y] : path)
    {
        if (isFirst)
        {
            isFirst = false;
            t.teleport(x, y);
            t.switchPen();
        }
        else
        {
            t.curveTo(x, y, Turtle::LEFT, Turtle::ARC);
        }
    }

    const std::string &curve = t.terminate();
    Path shape{curve, std::nullopt, outer};

    SVG svg{420, 370, {{"viewBox", "-1 -1 42 37"}, {"fill-opacity", "0"}}};
    svg.setData({shape});

    std::cout << svg << "\n";
}
