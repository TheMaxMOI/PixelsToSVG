#pragma once

#include "../element.hh"

class Path : public Element
{
public:
    Path(const std::string &path,
         std::optional<Outline> outer = std::nullopt);
};