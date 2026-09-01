#pragma once
#include "../../lib/svg/svg.hh"

enum class MutationKind
{
    Geometry,
    Appearance,
    SwapLayer,
    Add,
    Remove
};

class Mutator
{
public:
    Mutator(SVG& svg, int height, int width);

    SVG& get();

private:
    SVG& svg_;
    int height_, width_;

    void mutate();
    void swapLayer();
    void alterGeometry();
    void addShape();
    void alterAppearance();
    void removeShape();
};