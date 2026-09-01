#include <cstdlib>
#include <chrono>
#include <exception>
#include <iostream>
#include <string>

#include "../../lib/svg/svg.hh"
#include "config.hh"
#include "../randomize/randomSVG.hh"
#include "mutator.hh"
#include <opencv2/opencv.hpp>
#include <stdexcept>

cv::Mat getImage(const std::string& path = SRC_IMAGE_PATH) {
    cv::Mat targetImg = cv::imread(path, cv::IMREAD_UNCHANGED);

    if (targetImg.empty()) {
        throw std::runtime_error("Could not read image: " + path);
    }

    cv::Mat convertedImg;

    if (targetImg.channels() == 1) {
        cv::cvtColor(targetImg, convertedImg, cv::COLOR_GRAY2RGBA);
    } else if (targetImg.channels() == 4) {
        cv::cvtColor(targetImg, convertedImg, cv::COLOR_BGRA2RGBA);
    } else {
        cv::cvtColor(targetImg, convertedImg, cv::COLOR_BGR2RGBA);
    }

    return convertedImg;
}

SVG loopMutateAndScore(const cv:Mat& refImage, size_t height, size_t width, size_t iterations)
{
    const auto& scoring = [&refImage, height, width] (const SVG &svg) {mse(refImage, rasterize(svg, height, width))}

    SVG svg{width, height};
    double currScore = scoring(svg);

    #if PROGRESS_BAR
     // define and init progressBar
    #endif
    for (size_t i = 0; i < iterations; ++i)
    {
        SVG candidate = svg.copy();
        candidate = Mutator(candidate, height, width).get();

        const auto score = scoring(candidate);
        if (score < currScore) {
            currScore = score;
            svg = candidate;
        }

        #if PROGRESS_BAR
        // update and print progressBar
        #endif
    }

    return svg;
}

void summary(const SVG& svg, double elapsed, size_t iterations)
{
    std::cout << "Completed " << iterations << " iterations in " << elapsed
              << " seconds - avg time per iteration:" << elapsed / iterations << ".\n";
    std::cout << svg << '\n';
}

int main(int argc, char *argv[])
{
    const size_t width = MAX_WIDTH;
    const size_t height = MAX_HEIGHT;
    const size_t iterations = MAX_ITER;

    const auto & refImage = getImage();

    const auto start = std::chrono::steady_clock::now();
    SVG svg = loopMutateAndScore(refImage, height, width, iterations);
    const auto end = std::chrono::steady_clock::now();

    const std::chrono::duration<double> elapsed = end - start;

    summary(svg, elapsed.count(), iterations);
    return EXIT_SUCCESS;
}