#include "cursor.hh"

#include <format>

#include "../utils/concatStr.hh"
#include "../utils/doubleFormat.hh"

Cursor::Cursor(double x, double y)
    : x_{ x }
    , y_{ y }
{
    moveTo(x, y);
}

const std::pair<double, double> Cursor::getPosition() const
{
    return { x_, y_ };
}

void Cursor::moveTo(double x, double y)
{
    x_ = x;
    y_ = y;
    history_.push_back("M" + doubleFmt(x) + "," + doubleFmt(y));

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
    history_.push_back("L" + doubleFmt(x) + "," + doubleFmt(y));
}

void Cursor::horizontalTo(double x)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    history_.push_back("H" + doubleFmt(x));
}

void Cursor::verticalTo(double y)
{
    if (!editing_)
    {
        return;
    }

    y_ = y;
    history_.push_back("V" + doubleFmt(y));
}

void Cursor::quadraticTo(double cx, double cy, double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("Q" + doubleFmt(cx) + "," + doubleFmt(cy) + ","
                       + doubleFmt(x) + "," + doubleFmt(y));
}

void Cursor::cubicTo(double cx1, double cy1, double cx2, double cy2, double x,
                     double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("C" + doubleFmt(cx1) + "," + doubleFmt(cy1) + ","
                       + doubleFmt(cx2) + "," + doubleFmt(cy2) + ","
                       + doubleFmt(x) + "," + doubleFmt(y));
}

void Cursor::smoothQuadraticTo(double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("T" + doubleFmt(x) + "," + doubleFmt(y));
}

void Cursor::smoothCubicTo(double cx, double cy, double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("S" + doubleFmt(cx) + "," + doubleFmt(cy) + ","
                       + doubleFmt(x) + "," + doubleFmt(y));
}

void Cursor::ellipticalArcTo(double radius1, double radius2, double rot,
                             bool flip, bool sweep, double x, double y)
{
    if (!editing_)
    {
        return;
    }

    x_ = x;
    y_ = y;
    history_.push_back("A" + doubleFmt(radius1) + "," + doubleFmt(radius2) + ","
                       + doubleFmt(rot) + "," + std::to_string(flip) + ","
                       + std::to_string(sweep) + "," + doubleFmt(x) + ","
                       + doubleFmt(y));
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