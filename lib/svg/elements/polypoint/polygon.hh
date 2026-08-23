#pragma once

#include "polypoint.hh"

class Polygon : public Polypoint
{
public:
    Polygon(const std::vector<point_t> &points,
            std::optional<Coloring> inner = std::nullopt,
            std::optional<Outline> outer = std::nullopt);
};