#pragma once

#include <string>
#include <vector>

class Cursor
{
private:
    double x_;
    double y_;
    bool editing_ = false;
    std::vector<std::string> history_;

    std::string doubleFmt_(double x);

public:
    Cursor(double x, double y);

    const std::pair<double, double> getPosition() const;
    void moveTo(double x, double y);
    void lineTo(double x, double y);
    void horizontalTo(double x);
    void verticalTo(double y);
    void quadraticTo(double cx, double cy, double x, double y);
    void cubicTo(double cx1, double cy1, double cx2, double cy2, double x, double y);
    void smoothQuadraticTo(double x, double y);
    void smoothCubicTo(double cx, double cy, double x, double y);
    void ellipticalArcTo(double radius1, double radius2,
                         double rot,
                         bool flip, bool sweep,
                         double x, double y);
    void stopHere();
    std::string toPath();
};