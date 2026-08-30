#include <algorithm>
#include <iostream>

#include "../elements/appearance.hh"
#include "../elements/shapes/line.hh"
#include "../svg.hh"

int main(void)
{
    Outline outer{ "#ff0000", 1 };
    double sqrt3 = 1.732;

    std::vector<std::tuple<double, double>> vertices{
        { 1.5, sqrt3 }, { 0.5, sqrt3 }, { 0, sqrt3 / 2 },
        { 0.5, 0 },     { 1.5, 0 },     { 2, sqrt3 / 2 }
    };

    double scale = 20;
    std::transform(
        vertices.begin(), vertices.end(), vertices.begin(),
        [scale](
            const std::tuple<double, double>& p) -> std::tuple<double, double> {
            return { std::get<0>(p) * scale, std::get<1>(p) * scale };
        });

    Line l1{ vertices[0], vertices[1], outer };
    Line l2{ vertices[1], vertices[2], outer };
    Line l3{ vertices[2], vertices[3], outer };
    Line l4{ vertices[3], vertices[4], outer };
    Line l5{ vertices[4], vertices[5], outer };
    Line l6{ vertices[5], vertices[0], outer };

    SVG svg{ 420, 370, { { "viewBox", "-1 -1 42 37" } } };
    svg.setData({ l1, l2, l3, l4, l5, l6 });

    std::cout << svg << "\n";
}