#pragma once

#include "../element.hh"
#include <cstddef>

class Line : public Element
{
private:
    size_t  x1_;
    size_t  y1_;
    size_t  x2_;
    size_t  y2_;
public:
    Line(const std::tuple<size_t, size_t> &pos1,
         const std::tuple<size_t, size_t> &pos2,
         std::optional<Outline> outer);

    // static Line generate(size_t height, size_t width); // TODO
};