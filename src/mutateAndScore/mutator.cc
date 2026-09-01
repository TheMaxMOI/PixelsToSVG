#include "mutator.hh"

#include <algorithm>
#include <array>
#include <cmath>
#include <optional>
#include <random>

#include "../../lib/svg/svg.hh"
#include "../../lib/svg/elements/appearance.hh"
#include "../randomize/randomSVG.hh"


namespace {

std::mt19937& rng() {
    static thread_local std::mt19937 engine{std::random_device{}()};
    return engine;
} 

double round2(double v) { return std::round(v * 100.0) / 100.0; }

double opacityOr(const std::optional<Coloring>& c, double fallback) {
    return c.has_value() ? c->opacity : fallback;
}

double opacityOr(const std::optional<Outline>& o, double fallback) {
    return o.has_value() ? o->opacity : fallback;
}

double widthOr(const std::optional<Outline>& o, double fallback) {
    return o.has_value() ? o->width : fallback;
}

constexpr std::array<double, 5> kWeights = {0.40, 0.30, 0.15, 0.10, 0.05};

} // anonymous

Mutator::Mutator(SVG& svg, int height, int width)
    : svg_(svg), height_(height), width_(width) {
    mutate();
}

SVG& Mutator::get() {
    svg_.setData(svg_.data());
    return svg_;
}

void Mutator::mutate() {
    auto& elms = svg_.data();
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
    auto& elms = svg_.data();
    std::uniform_int_distribution<size_t> dist(0, elms.size() - 1);

    size_t idx1 = dist(rng());
    size_t idx2 = dist(rng());
    while (idx2 == idx1) idx2 = dist(rng());

    std::swap(elms[idx1], elms[idx2]);
}

void Mutator::alterGeometry() {
    auto& elms = svg_.data();
    std::uniform_int_distribution<size_t> pick(0, elms.size() - 1);
    auto& elm = elms[pick(rng())];

    std::uniform_int_distribution<int> jitter(-5, 5);

    if (auto* poly = dynamic_cast<Polygon*>(elm.get())) {
        std::uniform_int_distribution<size_t> ptDist(0, poly->positions().size() - 1);
        const size_t idx = ptDist(rng());
        const Point p = poly->positions()[idx];
        poly->updatePoint({p.x + jitter(rng()), p.y + jitter(rng())}, idx);

    } else if (auto* ell = dynamic_cast<Ellipse*>(elm.get())) {
        ell->changeCenter(ell->x + jitter(rng()), ell->y + jitter(rng()));

    } else if (auto* circ = dynamic_cast<Circle*>(elm.get())) {
        circ->changeCenter(circ->x + jitter(rng()), circ->y + jitter(rng()));

    } else if (auto* rect = dynamic_cast<Rectangle*>(elm.get())) {
        rect->changeTopLeftCorner(rect->x + jitter(rng()), rect->y + jitter(rng()));
    }
}

void Mutator::addShape() {
    auto factory = random_svg::getRandShapeFactory();
    svg_.data().push_back(factory(height_, width_));
}

void Mutator::alterAppearance() {
    auto& elms = svg_.data();
    std::uniform_int_distribution<size_t> pick(0, elms.size() - 1);
    auto& elm = elms[pick(rng())];

    std::uniform_int_distribution<int> colorDist(0, 255);
    const int r = colorDist(rng()), g = colorDist(rng()), b = colorDist(rng());

    std::bernoulli_distribution coin(0.5);
    std::uniform_real_distribution<double> deltaOpacity(-0.1, 0.1);

    if (coin(rng())) { // Coloring
        const double baseOpacity = opacityOr(elm->inner(), 0.0);
        const double opacity = std::clamp(baseOpacity + deltaOpacity(rng()), 0.05, 1.0);
        elm->updateColoring(Coloring(rgb(r, g, b), round2(opacity)));

    } else { // Outline
        const double baseOpacity = opacityOr(elm->outer(), 0.0);
        const double baseWidth = widthOr(elm->outer(), 0.0);

        std::uniform_real_distribution<double> deltaWidth(-0.5, 0.5);
        const double opacity = std::clamp(baseOpacity + deltaOpacity(rng()), 0.05, 1.0);
        const double width = std::max(0.5, baseWidth + deltaWidth(rng()));

        elm->updateOutline(Outline(rgb(r, g, b), round2(width), round2(opacity)));
    }
}

void Mutator::removeShape() {
    auto& elms = svg_.data();
    std::uniform_int_distribution<size_t> dist(0, elms.size() - 1);
    elms.erase(elms.begin() + dist(rng()));
}