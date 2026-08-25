#pragma once

#include <vector>
#include <string>
#include <tuple>

class Appearance
{
protected:
    const std::string coloring_key_;
    const std::string color_;
    double opacity_;

    Appearance(const std::string &coloring_key, const std::string &color, double opacity);
    std::string doubleFmt_(double x) const;

public:
    virtual ~Appearance() = default;

    virtual std::vector<std::tuple<std::string, std::string>> use() const;
};

class Outline : public Appearance
{
private:
    double width_;

public:
    Outline(const std::string &stroke, double width, double opacity = 1.0);

    std::vector<std::tuple<std::string, std::string>> use() const override;

    static Outline generate();
};

class Coloring : public Appearance
{
public:
    Coloring(const std::string &fill, double opacity = 1.0);

    static Coloring generate();
};