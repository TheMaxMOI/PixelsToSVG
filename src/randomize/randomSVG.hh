#pragma once
#include <cstddef>
#include <functional>
#include <vector>

#include "../../lib/svg/elements/round/circle.hh"
#include "../../lib/svg/elements/round/ellipse.hh"
#include "../../lib/svg/elements/shapes/line.hh"
#include "../../lib/svg/elements/shapes/rectangle.hh"
#include "../../lib/svg/svg.hh"

#define MIN_HEIGHT 16
#define MAX_HEIGHT 3096
#define MIN_WIDTH 16
#define MAX_WIDTH 4128

using ShapeFactory = std::function<Tag(size_t height, size_t width)>;

const std::vector<ShapeFactory>& shapeFactories();

std::vector<ShapeFactory> getRandShapeFactories(size_t amount);

ShapeFactory getRandShapeFactory();

SVG getSVG(size_t shapeAmount);