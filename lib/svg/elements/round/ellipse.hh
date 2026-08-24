#pragma once

#include "round.hh"
#include <cstddef>

class Ellipse : public Round
{
private:
    size_t rY_;

public:
    Ellipse(size_t rX,
            size_t rY,
            const std::tuple<size_t, size_t> &center = {0, 0},
            std::optional<Coloring> inner = std::nullopt,
            std::optional<Outline> outer = std::nullopt);

    static Ellipse generate(size_t height, size_t width);
};