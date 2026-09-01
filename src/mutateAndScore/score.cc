#include "score.hh"

#include <opencv2/core.hpp>

double mse(const cv::Mat& target, const cv::Mat& candidate) {
    CV_Assert(target.size() == candidate.size());
    CV_Assert(target.channels() == candidate.channels());

    cv::Mat t32, c32;
    target.convertTo(t32, CV_32F);
    candidate.convertTo(c32, CV_32F);

    cv::Mat diff = t32 - c32;
    diff = diff.mul(diff);

    cv::Scalar perChannelMean = cv::mean(diff);
    const int channels = target.channels();

    double total = 0.0;
    for (int c = 0; c < channels; ++c) total += perChannelMean[c];

    return total / channels;
}