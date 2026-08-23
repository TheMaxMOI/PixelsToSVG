#pragma once

#include "../element.hh"
#include <cstddef>

class Ellipse : public Element
{
private:
    size_t rX_;
    size_t rY_;
    size_t x_;
    size_t y_;

public:
    Ellipse(size_t rX,
            size_t rY,
            const std::tuple<size_t, size_t> &center = {0, 0},
            std::optional<Coloring> inner = std::nullopt,
            std::optional<Outline> outer = std::nullopt);

    // static Ellipse generate(size_t height, size_t width); // TODO

    void changeCenter(size_t x, size_t y);
};