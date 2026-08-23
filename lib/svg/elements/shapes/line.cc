#include "line.hh"

Line::Line(const std::tuple<size_t, size_t> &pos1,
           const std::tuple<size_t, size_t> &pos2,
           std::optional<Outline> outer)
    : Element{
          "line",
          {{"x1", std::to_string(std::get<0>(pos1))},
           {"y1", std::to_string(std::get<1>(pos1))},
           {"x2", std::to_string(std::get<0>(pos2))},
           {"y2", std::to_string(std::get<1>(pos2))}},
          std::nullopt,
          outer,
          true},
      x1_{std::get<0>(pos1)}, y1_{std::get<1>(pos1)}, x2_{std::get<0>(pos2)}, y2_{std::get<1>(pos2)}
{
}