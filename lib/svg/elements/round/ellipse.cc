#include "ellipse.hh"

#include "../utils/mathHelpers.hh"

Ellipse::Ellipse(size_t rX, size_t rY, const std::tuple<size_t, size_t>& center,
                 std::optional<Coloring> inner, std::optional<Outline> outer)
    : Round("ellipse",
            { { "rx", std::to_string(rX) },
              { "ry", std::to_string(rY) },
              { "x", std::to_string(std::get<0>(center)) },
              { "y", std::to_string(std::get<1>(center)) } },
            rX, center, inner, outer)
    , rY_{ rY }
{}

Ellipse Ellipse::generate(size_t height, size_t width)
{
    size_t max = MIN(height, width);
    size_t r1 = randint(max);
    size_t r2 = randint(max);
    size_t x = randint(width);
    size_t y = randint(height);

    return Ellipse(r1, r2, { x, y }, Coloring::generate(), Outline::generate());
}