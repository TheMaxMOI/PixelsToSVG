#include "declaration.hh"

#include <iostream>
#include <sstream>

Declaration::Declaration(const std::vector<attr_t>& attributes)
    : Tag{ "xml", attributes, true }
{
    for (const auto& [attrName, _] : attributes)
    {
        bool found = false;
        for (const auto& name : allowedAttributes_)
        {
            if (name == attrName)
            {
                found = true;
                break;
            }
        }
        if (!found)
        {
            throw std::logic_error(
                "Declaration: Declaration: invalid attribute (" + attrName
                + ")!");
        }
    }
}

void Declaration::print_(std::ostream& os) const
{
    if (!hasAttribute_(std::string{ mandatoryAttribute_ }))
    {
        throw std::logic_error("Declaration: print_: declaration must have "
                               + std::string{ mandatoryAttribute_ } + "!");
    }
    const auto version = getAttributeValue_("version");
    if (version != "1.0" && version != "1.1")
    {
        std::cerr << "You are using an unofficial version of XML\n";
    }
    const auto standalone = getAttributeValue_("standalone");
    if (standalone.has_value() && standalone != "yes" && standalone != "no")
    {
        throw std::logic_error(
            "Declaration: print_: The attribute \"standalone\" must have the "
            "value \"yes\" or \"no\"!");
    }

    std::stringstream growingString;
    growingString << static_cast<Tag>(*this);

    const std::string tagStr = growingString.str();

    os << tagStr.at(0) << '?' << tagStr.substr(1, tagStr.length() - 3) << '?'
       << tagStr.back();
}