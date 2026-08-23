#include "rgb.hh"

#include <format>

std::string rgb(uint8_t r, uint8_t g, uint8_t b)
{
    std::string rHEX = std::format("{:02X}", r);
    std::string gHEX = std::format("{:02X}", g);
    std::string bHEX = std::format("{:02X}", b);

    return "#" + rHEX + gHEX + bHEX;
}