#include "polygon.hh"

Polygon::Polygon(const std::vector<point_t>& points,
                 std::optional<Coloring> inner, std::optional<Outline> outer)
    : Polypoint("polygon", points, inner, outer)
{}