#include "appearance.hh"

#include <format>

#include "../../rgb/rgb.hh"
#include "utils/mathHelpers.hh"

Appearance::Appearance(const std::string &coloring_key, const std::string &color, double opacity)
    : coloring_key_{coloring_key}, color_{color}, opacity_{opacity}
{
}

std::string Appearance::doubleFmt_(double x) const
{
    return std::format("{:.2f}", x);
}

std::vector<std::tuple<std::string, std::string>> Appearance::use() const
{
    return {{coloring_key_, color_},
            {coloring_key_ + "-opacity", doubleFmt_(opacity_)}};
}

Coloring::Coloring(const std::string &fill, double opacity)
    : Appearance{"fill", fill, opacity}
{
}

Outline::Outline(const std::string &stroke, double width, double opacity)
    : Appearance{"stroke", stroke, opacity}, width_{width}
{
}

std::vector<std::tuple<std::string, std::string>> Outline::use() const
{
    auto attributes = Appearance::use();
    attributes.push_back({"stroke-width", doubleFmt_(width_)});

    return attributes;
}

Outline Outline::generate()
{
    const auto &color = rgb(randint(MAX_UINT8), randint(MAX_UINT8), randint(MAX_UINT8));
    return Outline(color, randint(10), round(my_random(), 2));
}

Coloring Coloring::generate()
{
    const auto &color = rgb(randint(MAX_UINT8), randint(MAX_UINT8), randint(MAX_UINT8));
    return Coloring(color, round(my_random(), 2));
}