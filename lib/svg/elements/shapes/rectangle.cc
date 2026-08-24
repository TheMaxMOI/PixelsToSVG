#include "rectangle.hh"

#include "../utils/mathHelpers.hh"

Rectangle::Rectangle(size_t width,
                     size_t height,
                     const std::tuple<size_t, size_t> &topLeftPos = {0, 0},
                     std::optional<Coloring> inner = std::nullopt,
                     std::optional<Outline> outer = std::nullopt)
    : Element("rect",
              {{"width", std::to_string(width)},
               {"height", std::to_string(height)},
               {"x", std::to_string(std::get<0>(topLeftPos))},
               {"y", std::to_string(std::get<1>(topLeftPos))}},
              inner,
              outer,
              true)
{
    const auto &rx = getAttributeValue_("rx");
    if (rx.has_value())
    {
        rx_ = std::stoi(rx.value());
    }

    const auto &ry = getAttributeValue_("ry");
    if (ry.has_value())
    {
        ry_ = std::stoi(ry.value());
    }
}

void Rectangle::changeTopLeftCorner(size_t x, size_t y)
{
    updateAttribute_({"x", std::to_string(x)});
    updateAttribute_({"y", std::to_string(y)});

    x_ = x;
    y_ = y;
}

void Rectangle::setCornerCurvatureX(size_t rx)
{
    updateAttribute_({"rx", std::to_string(rx)});

    rx_ = rx;
}

void Rectangle::setCornerCurvatureY(size_t ry)
{
    updateAttribute_({"ry", std::to_string(ry)});

    ry_ = ry;
}

Rectangle Rectangle::generate(size_t height, size_t width)
{
    size_t x = randint(width);
    size_t y = randint(height);
    size_t w = randint(width);
    size_t h = randint(height);

    return Rectangle(w, h, {x, y}, Coloring::generate(), Outline::generate());
}