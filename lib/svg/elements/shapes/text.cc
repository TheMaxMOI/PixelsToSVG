#include "text.hh"

TextElement::TextElement(const std::string &name,
                         const std::tuple<size_t, size_t> &bottomLeftPos,
                         std::optional<Coloring> inner,
                         std::optional<Outline> outer)
    : Element{name,
              {
                  {"x", std::to_string(std::get<0>(bottomLeftPos))},
                  {"y", std::to_string(std::get<1>(bottomLeftPos))},
              },
              inner,
              outer}
{
    const auto &rot = getAttributeValue_("rot");
    if (rot.has_value())
    {
        rot_ = std::stoi(rot.value());
    }
}

void TextElement::rotate(int degree)
{
    int n = degree % 360 + 360;
    rot_ = (rot_ + n) % 360;
}

Text::Text(const std::tuple<size_t, size_t> &bottomLeftPos,
           std::optional<Coloring> inner,
           std::optional<Outline> outer)
    : TextElement{"text", bottomLeftPos, inner, outer}
{
}

Tspan::Tspan(const std::tuple<size_t, size_t> &bottomLeftPos,
             std::optional<Coloring> inner,
             std::optional<Outline> outer)
    : TextElement("tspan", bottomLeftPos, inner, outer)
{
}