#include "element.hh"

#include <cstddef>

void Element::updateAttribute_(const attr_t &attr)
{
    const auto &[attrName, attrVal] = attr;

    for (size_t i = 0; i < attributes_.size(); i++)
    {
        const auto &[name, _] = attributes_.at(i);

        if (attrName == name)
        {
            attributes_[i] = attr;
            return;
        }
    }

    attributes_.push_back(attr);
}

void Element::updateColoring(const Coloring &inner)
{
    inner_.emplace(inner);

    for (const attr_t &attr : inner.use())
    {
        updateAttribute_(attr);
    }
}

void Element::updateOutline(const Outline &outer)
{
    outer_.emplace(outer);

    for (const attr_t &attr : outer.use())
    {
        updateAttribute_(attr);
    }
}

Element::Element(const std::string &name,
                 const std::vector<attr_t> &attributes,
                 std::optional<Coloring> inner,
                 std::optional<Outline> outer,
                 bool isEmpty)
    : Tag{name, attributes, isEmpty}
{
    if (inner.has_value())
    {
        updateColoring(inner.value());
    }

    if (outer.has_value())
    {
        updateOutline(outer.value());
    }
}

Element Element::generate(const std::string &name, bool isEmpty)
{
    return Element(name, {}, Coloring::generate(), Outline::generate(), isEmpty);
}