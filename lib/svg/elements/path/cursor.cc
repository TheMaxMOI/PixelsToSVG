#include "cursor.hh"

#include <format>

#include "../utils/concatStr.hh"

Cursor::Cursor(double x, double y)
    : x_{x}, y_{y}
{
    moveTo(x, y);
}

std::string Cursor::doubleFmt_(double x)
{
    return std::format("{:.3f}", x);
}

const std::pair<double, double> Cursor::getPosition() const
{
    return {x_, y_};
}

void Cursor::moveTo(double x, double y)
{
    x_ = x;
    y_ = y;
    history_.push_back("M" + doubleFmt_(x) + "," + doubleFmt_(y));

    editing_ = true;
}

void Cursor::lineTo(double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("L" + doubleFmt_(x) + "," + doubleFmt_(y));
}

void Cursor::horizontalTo(double x)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    history_.push_back("H" + doubleFmt_(x));
}

void Cursor::verticalTo(double y)
{
    if (!editing_)
    {
        return;
    }

    y_ = y;
    history_.push_back("V" + doubleFmt_(y));
}

void Cursor::quadraticTo(double cx, double cy, double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("Q" +
                       doubleFmt_(cx) + "," + doubleFmt_(cy) +
                       "," + doubleFmt_(x) + "," + doubleFmt_(y));
}

void Cursor::cubicTo(double cx1, double cy1, double cx2, double cy2, double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("C" +
                       doubleFmt_(cx1) + "," + doubleFmt_(cy1) + "," +
                       doubleFmt_(cx2) + "," + doubleFmt_(cy2) +
                       "," + doubleFmt_(x) + "," + doubleFmt_(y));
}

void Cursor::smoothQuadraticTo(double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("T" + doubleFmt_(x) + "," + doubleFmt_(y));
}

void Cursor::smoothCubicTo(double cx, double cy, double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("S" +
                       doubleFmt_(cx) + "," + doubleFmt_(cy) +
                       "," + doubleFmt_(x) + "," + doubleFmt_(y));
}

void Cursor::ellipticalArcTo(double radius1, double radius2,
                             double rot,
                             bool flip, bool sweep,
                             double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("A" +
                       doubleFmt_(radius1) + "," + doubleFmt_(radius2) + "," +
                       doubleFmt_(rot) + "," +
                       std::to_string(flip) + "," + std::to_string(sweep) + "," +
                       doubleFmt_(x) + "," + doubleFmt_(y));
}

void Cursor::stopHere()
{
    if (!editing_)
    {
        return;
    }

    editing_ = false;
    history_.push_back("Z");
}

std::string Cursor::toPath()
{
    if (editing_)
    {
        stopHere();
    }

    return joinWithSpace(history_);
}