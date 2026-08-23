#include "polyline.hh"

Polyline::Polyline(const std::vector<point_t> &points,
                   std::optional<Coloring> inner = std::nullopt,
                   std::optional<Outline> outer = std::nullopt)
    : Polypoint{"polyline", points, inner, outer}
{
}