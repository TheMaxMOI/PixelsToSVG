#include "polyline.hh"

Polyline::Polyline(const std::vector<point_t> &points,
                   std::optional<Coloring> inner,
                   std::optional<Outline> outer)
    : Polypoint{"polyline", points, inner, outer}
{
}