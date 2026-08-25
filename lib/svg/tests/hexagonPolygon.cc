#include "../svg.hh"
#include "../elements/appearance.hh"
#include "../elements/polypoint/polygon.hh"

#include <algorithm>
#include <iostream>

int main(void)
{
    Coloring inner{"#000000", 0};
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

    Polygon shape{vertices, inner, outer};

    SVG svg{420, 370, {{"viewBox", "-1 -1 42 37"}}};
    svg.setData({shape});

    std::cout << svg << "\n";
}
