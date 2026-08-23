#include "ellipse.hh"

Ellipse::Ellipse(size_t rX,
                 size_t rY,
                 const std::tuple<size_t, size_t> &center,
                 std::optional<Coloring> inner,
                 std::optional<Outline> outer)
    : Element("ellipse",
              {{"rx", std::to_string(rX)},
               {"ry", std::to_string(rY)},
               {"x", std::to_string(std::get<0>(center))},
               {"y", std::to_string(std::get<1>(center))}},
              inner,
              outer,
              true),
      rX_{rX},
      rY_{rY},
      x_{std::get<0>(center)}, y_{std::get<1>(center)}
{
}

void Ellipse::changeCenter(size_t x, size_t y)
{
    updateAttribute_({"cx", std::to_string(x)});
    updateAttribute_({"cy", std::to_string(y)});

    x_ = x;
    y_ = y;
}