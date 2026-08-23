#include "svg.hh"

SVG::SVG(size_t width, size_t height, const std::vector<attr_t> &additionalAttrs)
    : Tag("svg", additionalAttrs, false), width_{width}, height_{height}
{
    addAttribute({"width", std::to_string(width)});
    addAttribute({"height", std::to_string(height)});
    addAttribute({"xmlns", "http://www.w3.org/2000/svg"});
}

void SVG::generate(std::ostream &os) const {
    // checkTspan then throw error if needed

    Declaration d{{{"version", "1.0"}, {"encoding", "UTF-8"}}};
    
    os << d << "\n" << *this;
}

// void SVG::checkTspan() const; // TODO after Tspan