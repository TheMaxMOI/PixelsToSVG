#pragma once

#include "../element.hh"
#include <cstddef>

class Rectangle : public Element
{
private:
    size_t width_;
    size_t height_;
    size_t x_;
    size_t y_;
    size_t rx_ = 0;
    size_t ry_ = 0;

public:
    Rectangle(size_t width,
              size_t height,
              const std::tuple<size_t, size_t> &topLeftPos = {0, 0},
              std::optional<Coloring> inner = std::nullopt,
              std::optional<Outline> outer = std::nullopt);
            
    void changeTopLeftCorner(size_t x, size_t y);
    void setCornerCurvatureX(size_t rx);
    void setCornerCurvatureY(size_t ry);

    // static Rectangle generate(size_t height, size_t width); // TODO
};