#include "svg.hh"

#include <functional>

#include "elements/shapes/text.hh"

#define ISINSTANCE(tag, clazz) \
    (dynamic_cast<clazz *>(&tag) != nullptr)

SVG::SVG(size_t width, size_t height, const std::vector<attr_t> &additionalAttrs)
    : Tag("svg", additionalAttrs, false), width_{width}, height_{height}
{
    addAttribute({"width", std::to_string(width)});
    addAttribute({"height", std::to_string(height)});
    addAttribute({"xmlns", "http://www.w3.org/2000/svg"});
}

void SVG::generate(std::ostream &os) const
{
    // checkTspan then throw error if needed

    Declaration d{{{"version", "1.0"}, {"encoding", "UTF-8"}}};

    os << d << "\n"
       << *this;
}

bool SVG::checkTspan() const
{
    std::function<bool(Tag, std::optional<Tag>)> check;

    check = [&check](Tag tag, std::optional<Tag> parent) -> bool
    {
        if (ISINSTANCE(tag, Tspan))
        {
            if (!parent.has_value() ||
                !ISINSTANCE(parent.value(), Text) && !ISINSTANCE(parent.value(), Tspan))
            {
                return false;
            }
        }

        const auto &data = tag.getData();

        if (data.size() > 0)
        {
            for (const auto &variantChild : data)
            {
                if (!std::holds_alternative<Tag>(variantChild))
                {
                    continue;
                }

                auto child = std::get<Tag>(variantChild);
                if (!check(child, tag))
                {
                    return false;
                }
            }

            return true;
        }

        return true;
    };

    return check(*this, std::nullopt);
}