#pragma once

#include <optional>

#include "../../xmlGen/tag.hh"
#include "appearance.hh"

class Element : public Tag
{
private:
    std::optional<Coloring> inner_;
    std::optional<Outline> outer_;

protected:
    void updateAttribute_(const attr_t &attr);

public:
    Element(const std::string &name,
            const std::vector<attr_t> &attributes,
            std::optional<Coloring> inner = std::nullopt,
            std::optional<Outline> outer = std::nullopt,
            bool isEmpty = false);

    // static Element generate(const std::string& name, bool isEmpty); TODO

    void updateColoring(const Coloring &inner);
    void updateOutline(const Outline &outer);
};