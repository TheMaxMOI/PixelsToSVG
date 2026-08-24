#include "appearance.hh"

#include "../../rgb/rgb.hh"
#include "utils/mathHelpers.hh"

Appearance::Appearance(const std::string &coloring_key, const std::string &color, double opacity)
    : coloring_key_{coloring_key}, color_{color}, opacity_{opacity}
{
}

std::vector<std::tuple<std::string, std::string>> Appearance::use() const
{
    return {{coloring_key_, color_},
            {coloring_key_ + "-opacity", std::to_string(opacity_)}};
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
    attributes.push_back({"stroke-width", std::to_string(width_)});

    return attributes;
}

Outline Outline::generate()
{
    const auto &color = rgb(randint(MAX_UINT8), randint(MAX_UINT8), randint(MAX_UINT8));
    return Outline(color, randint(10), round(random(), 2));
}

Coloring Coloring::generate()
{
    const auto &color = rgb(randint(MAX_UINT8), randint(MAX_UINT8), randint(MAX_UINT8));
    return Coloring(color, round(random(), 2));
}