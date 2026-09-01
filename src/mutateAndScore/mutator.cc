#include "mutator.hh"

#include <algorithm>
#include <array>
#include <random>

#include "../randomize/randomSVG.hh"


namespace {

std::mt19937& rng() {
    static thread_local std::mt19937 engine{std::random_device{}()};
    return engine;
} 

constexpr std::array<double, 5> kWeights = {0.40, 0.30, 0.15, 0.10, 0.05};

} // anonymous

Mutator::Mutator(SVG& svg, int height, int width)
    : svg_(svg), height_(height), width_(width) {
    mutate();
}

SVG& Mutator::get() {
    return svg_;
}

void Mutator::mutate() {
    const auto elms = svg_.getData();
    if (elms.empty()) {
        addShape();
        return;
    }

    std::discrete_distribution<int> dist(kWeights.begin(), kWeights.end());
    const auto strategy = static_cast<MutationKind>(dist(rng()));

    if (strategy == MutationKind::SwapLayer && elms.size() >= 2) {
        swapLayer();
    } else if (strategy == MutationKind::Geometry) {
        alterGeometry();
    } else if (strategy == MutationKind::Appearance) {
        alterAppearance();
    } else if (strategy == MutationKind::Add) {
        addShape();
    } else if (strategy == MutationKind::Remove && elms.size() > 1) {
        removeShape();
    } else {
        alterGeometry();
    }
}

void Mutator::swapLayer() {
    auto elms = svg_.getData();
    std::uniform_int_distribution<size_t> dist(0, elms.size() - 1);

    size_t idx1 = dist(rng());
    size_t idx2 = dist(rng());
    while (idx2 == idx1) idx2 = dist(rng());

    std::swap(elms[idx1], elms[idx2]);
    svg_.setData(elms);
}

void Mutator::alterGeometry() {
}

void Mutator::addShape() {
    auto factory = getRandShapeFactory();
    auto elms = svg_.getData();
    elms.push_back(factory(height_, width_));
    svg_.setData(elms);
}

void Mutator::alterAppearance() {
}

void Mutator::removeShape() {
    auto elms = svg_.getData();
    std::uniform_int_distribution<size_t> dist(0, elms.size() - 1);
    elms.erase(elms.begin() + dist(rng()));
    svg_.setData(elms);
}