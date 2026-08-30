#pragma once

#include "tag.hh"

template <Callable TagFunc>
void Tag::visit(TagFunc f) const
{
    f(*this);

    if (isEmpty_)
    {
        return;
    }

    for (const data_t& child : data_)
    {
        if (std::holds_alternative<Tag>(child))
        {
            std::get<Tag>(child).visit(f);
        }
    }
}
