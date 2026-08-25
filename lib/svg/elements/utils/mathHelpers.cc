#include "mathHelpers.hh"

#include <cmath>
#include <random>
#include <algorithm>

const double a = 2.0 * std::numbers::pi / 3.0;
const double I = (3.0 / std::numbers::pi) * std::log(2.0 + std::sqrt(3.0)) - 0.96;
const double K = 1.0 / I;
const double LN_2_PLUS_SQRT_3 = std::log(2.0 + std::sqrt(3.0));

std::mt19937_64 &getRDMengine()
{
    thread_local std::mt19937_64 engine(std::random_device{}());
    return engine;
}

double my_round(double x, int p)
{
    double powOf10 = std::pow(10.0, p);
    double val = std::floor(x * powOf10) / powOf10;

    return std::round(val * 1000.0) / 1000.0;
}

Rounder::Rounder(int p)
    : precision_{p}
{
}

std::pair<double, double> Rounder::operator()(double x, double y)
{
    double newX = my_round(dx_ + x, precision_);
    double newY = my_round(dy_ + y, precision_);
    dx_ += x - newX;
    dy_ += y - newY;
    return {newX, newY};
}

double my_sin(double degree)
{
    return std::sin(degree * std::numbers::pi / 180.0);
}

double my_cos(double degree)
{
    return std::cos(degree * std::numbers::pi / 180.0);
}

double norm2(const std::array<double, 2> &v)
{
    return std::hypot(v[0], v[1]);
}

double dist2(const std::array<double, 2> &a, const std::array<double, 2> &b)
{
    return std::hypot(a[0] - b[0], a[1] - b[1]);
}

double normInf(const std::array<double, 2> &v)
{
    return std::max(std::abs(v[0]), std::abs(v[1]));
}

double distInf(const std::array<double, 2> &a, const std::array<double, 2> &b)
{
    return std::max(std::abs(a[0] - b[0]), std::abs(a[1] - b[1]));
}

int randint(int a, int b)
{
    std::uniform_int_distribution<int> dist(a, b);
    return dist(getRDMengine());
}

int randint(int max)
{
    return randint(0, max);
}

double f(double x)
{
    return K * (1.0 / (a * (x - 0.5)) - 0.96);
}

double F(double x)
{
    double u = a * (x - 0.5);
    return K * ((1.0 / a) * (std::log(1.0 / std::cos(u) + std::tan(u)) + LN_2_PLUS_SQRT_3) - 0.96 * x);
}

double my_random()
{
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    double u = dist(getRDMengine());
    double x = u;
    constexpr double eps = 1e-9;

    for (int i = 0; i < 6; ++i)
    {
        if (std::abs(x - 0.5) < eps)
        {
            x += eps;
        }

        double fx = f(x);
        if (fx != 0.0)
        {
            x -= (F(x) - u) / fx;
        }

        x = std::clamp(x, eps, 1.0 - eps);
    }
    return x;
}

double round(double x, size_t precision)
{
    size_t pow10 = std::pow(10, precision);
    return floor(x * pow10) / pow10;
}