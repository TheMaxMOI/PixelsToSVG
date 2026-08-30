#pragma once

#include <array>
#include <cstddef>

#define MIN(a, b) ((a < b) ? a : b)

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

double my_sin(double degree);
double my_cos(double degree);
double dist2(const std::array<double, 2>& a, const std::array<double, 2>& b);
double distInf(const std::array<double, 2>& a, const std::array<double, 2>& b);
int randint(int a, int b);
int randint(int max);
double my_random();
double round(double x, size_t precision);