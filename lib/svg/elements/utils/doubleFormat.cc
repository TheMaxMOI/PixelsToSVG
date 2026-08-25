#include "doubleFormat.hh"

#include <format>

std::string doubleFmt(double x, size_t precision)
{
    return std::format("{:.{}f}", x, precision);
}