#pragma once

#include "../element.hh"
#include <cstddef>

using point_t = std::tuple<size_t, size_t>;

class Polypoint : Element
{
private:
    std::vector<point_t> points_;
    std::vector<std::string> pointsRepr_;

    std::string joinWithSpace_(const std::vector<std::string> pointsRepr);
    std::string stringify_(const point_t &p) const;
    std::string stringify_(const std::vector<point_t> &points) const;

protected:
    Polypoint(const std::string &name,
              const std::vector<point_t> &points,
              std::optional<Coloring> inner = std::nullopt,
              std::optional<Outline> outer = std::nullopt);

public:
    void popPoint();
    void addPoint(point_t p);
    void insertPoint(point_t p, size_t i);
    void removePoint(size_t i);
    void updatePoint(point_t p, size_t i);
};