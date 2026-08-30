#pragma once

#include <cstddef>

#include "../utils/mathHelpers.hh"
#include "cursor.hh"

class Turtle
{
public:
    enum PenPosition
    {
        UP = 0,
        DOWN
    };

    enum Side
    {
        LEFT = 0,
        RIGHT
    };

    enum Curve
    {
        QUADRATIC = 0,
        CUBIC,
        SMOOTH_Q,
        SMOOTH_C,
        ARC,
    };

private:
    double x_;
    double y_;
    size_t rot_;
    PenPosition penPos_ = UP;
    Cursor cursor_;
    Rounder round_;

    std::pair<double, double> sidewaysOffset_(double dist, Side side);
    std::pair<double, double> forwardOffset_(double dist);

public:
    Turtle(double x = 0., double y = 0., size_t rot = 0, size_t precision = 3);

    Turtle& switchPen();
    PenPosition getPenPosition();
    size_t getRotation();
    const std::pair<double, double> getPosition();
    Turtle& rotate(int degree);
    Turtle& teleport(double x, double y);
    Turtle& move(double dist);
    Turtle& curveTo(double x, double y, Side side = LEFT,
                    Curve type = QUADRATIC);
    std::string terminate();
};