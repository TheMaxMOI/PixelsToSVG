#include "fastRasterizer.hh"

#include <algorithm>
#include <cmath>

#include "../../lib/rgb/rgb.hh"

void blendOver(cv::Mat& canvas, const cv::Mat& mask, const cv::Vec3f& colorRGB, double opacity) {
    if (opacity <= 0.0) return;
    if (cv::countNonZero(mask) == 0) return;

    CV_Assert(canvas.type() == CV_8UC4);
    CV_Assert(mask.type() == CV_8UC1);
    CV_Assert(canvas.size() == mask.size());

    const double srcA = opacity;

    for (int y = 0; y < canvas.rows; ++y) {
        for (int x = 0; x < canvas.cols; ++x) {
            if (!mask.at<uint8_t>(y, x)) continue;

            cv::Vec4b& px = canvas.at<cv::Vec4b>(y, x);

            const double dstA = px[3] / 255.0;
            const double outA = srcA + dstA * (1.0 - srcA);

            const cv::Vec3d dstRGB(px[0], px[1], px[2]);
            const cv::Vec3d srcRGB(colorRGB[0], colorRGB[1], colorRGB[2]);
            const cv::Vec3d blended = srcRGB * srcA + dstRGB * dstA * (1.0 - srcA);

            cv::Vec3d outRGB(0.0, 0.0, 0.0);
            if (outA > 1e-6) {
                outRGB = blended / outA;
            }

            px[0] = static_cast<uint8_t>(std::clamp(outRGB[0], 0.0, 255.0));
            px[1] = static_cast<uint8_t>(std::clamp(outRGB[1], 0.0, 255.0));
            px[2] = static_cast<uint8_t>(std::clamp(outRGB[2], 0.0, 255.0));
            px[3] = static_cast<uint8_t>(std::clamp(outA * 255.0, 0.0, 255.0));
        }
    }
}

std::optional<cv::Rect> clipBB(const lib::BBox& bbox, int height, int width) {
    int x0 = std::max(0, static_cast<int>(bbox.x0));
    int y0 = std::max(0, static_cast<int>(bbox.y0));
    int x1 = std::min(width, static_cast<int>(bbox.x1));
    int y1 = std::min(height, static_cast<int>(bbox.y1));

    if (x1 <= x0 || y1 <= y0) return std::nullopt;
    return cv::Rect(x0, y0, x1 - x0, y1 - y0);
}

void rasterizeShape(const Shape& shape, cv::Mat& canvas, int height, int width) {
    auto clipped = clipBB(shape.boundingBox(), height, width);
    if (!clipped) return;

    cv::Rect region = *clipped;
    cv::Mat view = canvas(region);

    if (shape.inner().has_value()) {
        cv::Mat mask = cv::Mat::zeros(region.height, region.width, CV_8UC1);
        shape.paintOnMask(mask, /*filled=*/true, region.tl());
        blendOver(view, mask, lib::hexToRGB(shape.inner()->color), shape.inner()->opacity);
    }

    if (shape.outer().has_value()) {
        cv::Mat mask = cv::Mat::zeros(region.height, region.width, CV_8UC1);
        shape.paintOnMask(mask, false, region.tl());
        blendOver(view, mask, lib::hexToRGB(shape.outer()->color), shape.outer()->opacity);
    }
}

cv::Mat rasterize(const SVG& svg, size_t height, size_t width) {
    cv::Mat canvas = cv::Mat::zeros(height, width, CV_8UC4);
    for (const auto& elm : svg.data()) {
        rasterizeShape(*elm, canvas, height, width);
    }
    return canvas;
}