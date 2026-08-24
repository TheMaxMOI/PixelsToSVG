#pragma once

#include "round.hh"
#include <cstddef>

class Circle : public Round
{
public:
    Circle(size_t radius,
           const std::tuple<size_t, size_t> &center = {0, 0},
           std::optional<Coloring> inner = std::nullopt,
           std::optional<Outline> outer = std::nullopt);

    static Circle generate(size_t height, size_t width);
};