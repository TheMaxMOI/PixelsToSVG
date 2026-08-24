#include "ellipse.hh"

Ellipse::Ellipse(size_t rX,
                 size_t rY,
                 const std::tuple<size_t, size_t> &center,
                 std::optional<Coloring> inner,
                 std::optional<Outline> outer)
    : Round("ellipse",
            {{"rx", std::to_string(rX)},
             {"ry", std::to_string(rY)},
             {"x", std::to_string(std::get<0>(center))},
             {"y", std::to_string(std::get<1>(center))}},
            rX,
            center,
            inner,
            outer),
      rY_{rY}
{
}