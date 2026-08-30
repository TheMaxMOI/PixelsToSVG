#include "circle.hh"

#include "../utils/mathHelpers.hh"

Circle::Circle(size_t radius, const std::tuple<size_t, size_t>& center,
               std::optional<Coloring> inner, std::optional<Outline> outer)
    : Round("circle",
            { { "r", std::to_string(radius) },
              { "x", std::to_string(std::get<0>(center)) },
              { "y", std::to_string(std::get<1>(center)) } },
            radius, center, inner, outer)
{}

Circle Circle::generate(size_t height, size_t width)
{
    size_t r = randint(MIN(height, width));
    size_t x = randint(width);
    size_t y = randint(height);

    return Circle(r, { x, y }, Coloring::generate(), Outline::generate());
}