#pragma once

#include <cstddef>

#include "../xmlGen/declaration.hh"
#include "../xmlGen/tag.hh"

class SVG : public Tag
{
private:
    size_t width_;
    size_t height_;

    virtual void print_(std::ostream& os) const override;

public:
    SVG(size_t width, size_t height,
        const std::vector<attr_t>& additionalAttrs = {});

    bool checkTspan() const;
};