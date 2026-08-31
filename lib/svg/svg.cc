#include "svg.hh"

#include <functional>

#include "../xmlGen/declaration.hh"
#include "elements/shapes/text.hh"

/* it is done like this rather a downcast (dynamic cast)
because containers' definitions would have to be changed
currently we're loosing information by pushing the element
by value.
Lazy fix is assert with name. True maintainable code would
change value to ptr to not loose this extra information.

TODO: optional
*/
#define ISINSTANCE(tag, clazz) (tag.getName() == clazz)

SVG::SVG(size_t width, size_t height,
         const std::vector<attr_t>& additionalAttrs)
    : Tag("svg", additionalAttrs, false)
    , width_{ width }
    , height_{ height }
{
    addAttribute({ "width", std::to_string(width) });
    addAttribute({ "height", std::to_string(height) });
    addAttribute({ "xmlns", "http://www.w3.org/2000/svg" });
}

void SVG::print_(std::ostream& os) const
{
    if (!checkTspan())
    {
        throw std::logic_error("SVG: print_: Tspan instances must be children "
                               "of other Tspan or Text instances!");
    }

    Declaration d{ { { "version", "1.0" }, { "encoding", "UTF-8" } } };

    os << d << "\n" << static_cast<Tag>(*this);
}

bool SVG::checkTspan() const
{
    std::function<bool(Tag, std::optional<Tag>)> check;

    check = [&check](Tag tag, std::optional<Tag> parent) -> bool {
        if (ISINSTANCE(tag, "tspan"))
        {
            if (!parent.has_value() || (!ISINSTANCE(parent.value(), "text") && !ISINSTANCE(parent.value(), "tspan")))
            {
                return false;
            }
        }

        const auto& data = tag.getData();

        if (data.size() == 0)
        {
            return true;
        }

        for (const auto& variantChild : data)
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
    };

    return check(*this, std::nullopt);
}