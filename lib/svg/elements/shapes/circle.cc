#include "circle.hh"

Circle::Circle(size_t radius,
               const std::tuple<size_t, size_t> &center,
               std::optional<Coloring> inner,
               std::optional<Outline> outer)
    : Element("circle",
              {{"r", std::to_string(radius)},
               {"x", std::to_string(std::get<0>(center))},
               {"y", std::to_string(std::get<1>(center))}},
              inner,
              outer,
              true),
      r_{radius}, x_{std::get<0>(center)}, y_{std::get<1>(center)}
{
}

void Circle::changeCenter(size_t x, size_t y)
{
    updateAttribute_({"cx", std::to_string(x)});
    updateAttribute_({"cy", std::to_string(y)});

    x_ = x;
    y_ = y;
}