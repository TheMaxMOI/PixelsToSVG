#include "polygon.hh"

Polygon::Polygon(const std::vector<point_t> &points,
                 std::optional<Coloring> inner = std::nullopt,
                 std::optional<Outline> outer = std::nullopt)
    : Polypoint("polygon", points, inner, outer)
{
}