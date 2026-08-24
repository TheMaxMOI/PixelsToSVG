#include "turtle.hh"

Turtle::Turtle(double x = 0., double y = 0.,
               size_t rot = 0, size_t precision = 3)
    : x_{x}, y_{y}, rot_{rot}, cursor_{Cursor(x, y)}, round_{Rounder(precision)}
{
}

Turtle &Turtle::switchPen()
{
    penPos_ = (penPos_ == UP) ? DOWN : UP;

    return *this;
}

Turtle::PenPosition Turtle::getPenPosition()
{
    return penPos_;
}

size_t Turtle::getRotation()
{
    return rot_;
}

const std::pair<double, double> &Turtle::getPosition()
{
    return {x_, y_};
}

Turtle &Turtle::rotate(int degree)
{
    int angle = degree % 360 + 360;
    rot_ = (rot_ + angle) % 360;

    return *this;
}

Turtle &Turtle::teleport(double x, double y)
{
    switch (penPos_)
    {
    case UP:
        cursor_.moveTo(x, y);
        break;
    case DOWN:
        if (x_ == x)
        {
            cursor_.verticalTo(y);
        }
        else if (y_ == y)
        {
            cursor_.horizontalTo(x);
        }
        else
        {
            cursor_.lineTo(x, y);
        }
        break;
    }

    const auto [x, y] = cursor_.getPosition();
    x_ = x;
    y_ = y;

    return *this;
}

Turtle &Turtle::move(double dist)
{
    const auto [dx, dy] = round_(dist * cos(rot_), dist * sin(rot_));

    return teleport(x_ + dx, y_ + dy);
}

std::string Turtle::terminate()
{
    cursor_.stopHere();
    return cursor_.toPath();
}

std::pair<double, double> Turtle::sidewaysOffset_(double dist, Side side)
{
    double direction = (side == RIGHT) ? -1. : 1.;

    double offsetX = direction * -sin(rot_) * dist;
    double offsetY = direction * cos(rot_) * dist;

    return {offsetX, offsetY};
}

std::pair<double, double> Turtle::forwardOffset_(double dist)
{
    double offsetX = cos(rot_) * dist;
    double offsetY = sin(rot_) * dist;

    return {offsetX, offsetY};
}

Turtle &Turtle::curveTo(double x, double y, Side side, Curve type)
{
    if (penPos_ == UP)
    {
        return teleport(x, y);
    }

    double distance = 0.;
    double radius = 0.;

    if (type < ARC)
        distance = dist2({x_, y_}, {x, y});
    else
        radius = distInf({x_, y_}, {x, y});

    if (type == QUADRATIC)
    {
        distance /= 2.;

        std::pair<double, double> offset = sidewaysOffset_(distance, side);

        double controlX = x_ + (x - x_) / 2. + offset.first;
        double controlY = y_ + (y - y_) / 2. + offset.second;

        cursor_.quadraticTo(controlX, controlY, x, y);
    }
    else if (type == CUBIC)
    {
        distance /= 3.;

        std::pair<double, double> normal = sidewaysOffset_(distance, side);
        std::pair<double, double> forward = forwardOffset_(distance);

        double control1X = x_ + forward.first + normal.first;
        double control1Y = y_ + forward.second + normal.second;
        double control2X = x - forward.first + normal.first;
        double control2Y = y - forward.second + normal.second;

        cursor_.cubicTo(control1X, control1Y, control2X, control2Y, x, y);
    }
    else if (type == SMOOTH_Q)
    {
        cursor_.smoothQuadraticTo(x, y);
    }
    else if (type == SMOOTH_C)
    {
        distance /= 3.;

        std::pair<double, double> normal = sidewaysOffset_(distance, side);
        std::pair<double, double> forward = forwardOffset_(distance);

        double controlX = x - forward.first + normal.first;
        double controlY = y - forward.second + normal.second;

        cursor_.smoothCubicTo(controlX, controlY, x, y);
    }
    else if (type == ARC)
    {
        radius /= 2.;
        bool sweep = (side == RIGHT);

        cursor_.ellipticalArcTo(radius, radius, 0., false, sweep, x, y);
    }

    const auto [x, y] = cursor_.getPosition();
    x_ = x;
    y_ = y;

    return *this;
}