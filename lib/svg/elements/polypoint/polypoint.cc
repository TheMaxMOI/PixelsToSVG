#include "polypoint.hh"

#include <sstream>

std::string Polypoint::joinWithSpace_(const std::vector<std::string> pointsRepr)
{
    std::stringstream growingString;

    bool isFirst = true;
    for (const auto &pointRepr : pointsRepr)
    {
        if (isFirst)
        {
            isFirst = false;
        }
        else
        {
            growingString << ' ';
        }

        growingString << pointRepr;
    }

    return growingString.str();
}

std::string Polypoint::stringify_(const point_t &p) const
{
    auto [x, y] = p;

    return std::to_string(x) + ',' + std::to_string(y);
}

std::string Polypoint::stringify_(const std::vector<point_t> &points) const
{
    std::stringstream growingString;

    bool isFirst = true;
    for (const auto &p : points)
    {
        if (isFirst)
        {
            isFirst = false;
        }
        else
        {
            growingString << ' ';
        }

        growingString << stringify_(p);
    }

    return growingString.str();
}

Polypoint::Polypoint(const std::string &name,
                     const std::vector<point_t> &points,
                     std::optional<Coloring> inner,
                     std::optional<Outline> outer)
    : Element{name,
              {{"points", stringify_(points)}},
              inner,
              outer,
              true}
{
    for (const auto &p : points)
    {
        pointsRepr_.push_back(stringify_(p));
    }
}

void Polypoint::popPoint()
{
    points_.pop_back();
    pointsRepr_.pop_back();
    updateAttribute_({"points", joinWithSpace_(pointsRepr_)});
}

void Polypoint::addPoint(point_t p)
{
    points_.push_back(p);
    pointsRepr_.push_back(stringify_(p));
    updateAttribute_({"points", joinWithSpace_(pointsRepr_)});
}

void Polypoint::insertPoint(point_t p, size_t i)
{
    if (i < points_.size())
    {
        points_.insert(points_.begin() + i, p);
        pointsRepr_.insert(pointsRepr_.begin() + i, stringify_(p));
    }
    else
    {
        points_.push_back(p);
        pointsRepr_.push_back(stringify_(p));
    }

    updateAttribute_({"points", joinWithSpace_(pointsRepr_)});
}
void Polypoint::removePoint(size_t i)
{
    if (i >= points_.size())
    {
        throw std::logic_error("Polypoint: removePoint: Out of range index to remove point!");
    }

    points_.erase(points_.begin() + i);
    pointsRepr_.erase(pointsRepr_.begin() + i);
    updateAttribute_({"points", joinWithSpace_(pointsRepr_)});
}

void Polypoint::updatePoint(point_t p, size_t i)
{
    if (i >= points_.size())
    {
        throw std::logic_error("Polypoint: updatePoint: Out of range index to update point!");
    }

    points_[i] = p;
    pointsRepr_[i] = stringify_(p);
    updateAttribute_({"points", stringify_(points_)});
    updateAttribute_({"points", joinWithSpace_(pointsRepr_)});
}
