#pragma once

#include <opencv2/core.hpp>
#include <optional>

#include "../../lib/svg/svg.hh"

void blendOver(cv::Mat& canvas, const cv::Mat& mask, const cv::Vec3f& colorRGB,
               double opacity);

std::optional<cv::Rect> clipBB(const BBox& bbox, int height, int width);

void rasterizeShape(const Shape& shape, cv::Mat& canvas, int height, int width);

cv::Mat rasterize(const SVG& svg, int height, int width);