#include <iostream>

#include "../elements/appearance.hh"
#include "../elements/path/path.hh"
#include "../elements/path/turtle.hh"
#include "../svg.hh"

int main(void)
{
    Coloring inner{ "#000000", 0 };
    Outline outer{ "#ff0000", 1 };
    auto len = 20ULL;
    int angle = 60;

    Turtle t{ 11, 0, 120 };
    t.switchPen();
    for (int i = 0; i < 6; i++)
    {
        t.move(len).rotate(-angle);
    }

    const auto& curve = t.terminate();
    Path shape{ curve, inner, outer };

    SVG svg{ 420, 370, { { "viewBox", "0 -1 43 37" } } };
    svg.setData({ shape });

    std::cout << svg << "\n";
}