#pragma once

#include "../element.hh"
#include <cstddef>
#include <string>
#include <tuple>
#include <vector>

class Round : public Element
{
protected:
    size_t r_;
    size_t x_;
    size_t y_;

public:
    Round(const std::string &name,
          const std::vector<attr_t> &attributes,
          size_t radius,
          const std::tuple<size_t, size_t> &center = {0, 0},
          std::optional<Coloring> inner = std::nullopt,
          std::optional<Outline> outer = std::nullopt);

    void changeCenter(size_t x, size_t y);
};