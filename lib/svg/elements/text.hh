#pragma once

#include <cstddef>

#include "element.hh"

class TextElement : public Element
{
private:
    size_t x_;
    size_t y_;
    size_t rot_ = 0;

protected:
    TextElement(const std::string &name,
                const std::tuple<size_t, size_t> &bottomLeftPos = {0, 0},
                std::optional<Coloring> inner = std::nullopt,
                std::optional<Outline> outer = std::nullopt);

public:
    void rotate(int degree);
};

class Text : public TextElement
{
public:
    Text(const std::tuple<size_t, size_t> &bottomLeftPos = {0, 0},
         std::optional<Coloring> inner = std::nullopt,
         std::optional<Outline> outer = std::nullopt);
};

class Tspan : public TextElement
{
public:
    Tspan(const std::tuple<size_t, size_t> &bottomLeftPos = {0, 0},
          std::optional<Coloring> inner = std::nullopt,
          std::optional<Outline> outer = std::nullopt);
};