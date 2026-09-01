#include "randomSVG.hh"

#include <random>

namespace {

std::mt19937& rng() {
    static thread_local std::mt19937 engine{std::random_device{}()};
    return engine;
}

} // anonymous

const std::vector<ShapeFactory>& shapeFactories() {
    static const std::vector<ShapeFactory> factories = {
        [](size_t h, size_t w) { return Tag{Circle::generate(h, w)}; },
        [](size_t h, size_t w) { return Tag{Ellipse::generate(h, w)}; },
        [](size_t h, size_t w) { return Tag{Line::generate(h, w)}; },
        [](size_t h, size_t w) { return Tag{Rectangle::generate(h, w)}; },
    };
    return factories;
}

std::vector<ShapeFactory> getRandShapeFactories(size_t amount) {
    std::vector<ShapeFactory> result;
    if (amount <= 0) return result;

    const auto& pool = shapeFactories();
    std::uniform_int_distribution<size_t> dist(0, pool.size() - 1);

    result.reserve(static_cast<size_t>(amount));
    for (size_t i = 0; i < amount; ++i) result.push_back(pool[dist(rng())]);
    return result;
}

ShapeFactory getRandShapeFactory() {
    const auto& pool = shapeFactories();
    std::uniform_int_distribution<size_t> dist(0, pool.size() - 1);
    return pool[dist(rng())];
}

SVG getSVG(size_t shapeAmount) {
    std::uniform_int_distribution<size_t> hDist(MIN_HEIGHT, MAX_HEIGHT - 1);
    std::uniform_int_distribution<size_t> wDist(MIN_WIDTH, MAX_WIDTH - 1);
    const size_t h = hDist(rng());
    const size_t w = wDist(rng());

    std::vector<data_t> data;
    data.reserve(static_cast<size_t>(shapeAmount));
    for (const auto& factory : getRandShapeFactories(shapeAmount)) {
        data.push_back(factory(h, w));
    }

    SVG svg(w, h);
    svg.setData(std::move(data));
    return svg;
}