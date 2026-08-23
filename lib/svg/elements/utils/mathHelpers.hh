#pragma once

#include <array>

class Rounder
{
private:
    double dx_ = 0.0;
    double dy_ = 0.0;
    int precision_;

public:
    explicit Rounder(int p = 0);

    std::pair<double, double> operator()(double x, double y);
};

inline double sin(double degree);
inline double cos(double degree);
inline double dist2(const std::array<double, 2> &a, const std::array<double, 2> &b);
inline double distInf(const std::array<double, 2> &a, const std::array<double, 2> &b);
inline int randint(int a, int b);
inline int randint(int max);
inline double random();