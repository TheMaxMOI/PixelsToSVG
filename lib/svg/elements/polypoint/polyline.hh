#pragma once

#include "polypoint.hh"

class Polyline : public Polypoint
{
public:
    Polyline(const std::vector<point_t> &points,
             std::optional<Coloring> inner = std::nullopt,
             std::optional<Outline> outer = std::nullopt);
};