#pragma once

#include "../element.hh"
#include <cstddef>

class Circle : public Element
{
private:
    size_t r_;
    size_t x_;
    size_t y_;

public:
    Circle(size_t radius,
           const std::tuple<size_t, size_t> &center = {0, 0},
           std::optional<Coloring> inner = std::nullopt,
           std::optional<Outline> outer = std::nullopt);

    // static Circle generate(size_t height, size_t width); // TODO

    void changeCenter(size_t x, size_t y);
};