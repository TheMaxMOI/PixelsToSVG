#pragma once

#include <array>

#include "tag.hh"

class Declaration : public Tag
{
private:
    const std::array<std::string_view, 3> allowedAttributes_{ "version",
                                                              "encoding",
                                                              "standalone" };
    const std::string_view mandatoryAttribute_{ "version" };

    virtual void print_(std::ostream& os) const override;

public:
    Declaration(const std::vector<attr_t>& attributes);
};