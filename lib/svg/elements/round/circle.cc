#include "circle.hh"

Circle::Circle(size_t radius,
               const std::tuple<size_t, size_t> &center,
               std::optional<Coloring> inner,
               std::optional<Outline> outer)
    : Round("circle",
            {{"r", std::to_string(radius)},
             {"x", std::to_string(std::get<0>(center))},
             {"y", std::to_string(std::get<1>(center))}},
            radius,
            center,
            inner,
            outer)
{
}