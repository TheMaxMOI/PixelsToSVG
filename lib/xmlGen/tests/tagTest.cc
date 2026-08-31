#include "../tag.hh"

#include <cassert>
#include <sstream>

void errorDupAttributesInit()
{
    bool res;
    try
    {
        res = false;
        Tag g{ "g", { { "id", "bottom" }, { "id", "left" } } };
    }
    catch (const std::logic_error& e)
    {
        res = true;
    }

    assert(res);
}

void emptyTag()
{
    Tag r{ "rect", {}, true };

    std::stringstream repr;
    repr << r;

    assert("<rect/>" == repr.str());
}

void dataEmptyTag()
{
    Tag r{ "rect", {}, true };

    bool res;
    try
    {
        res = false;
        r.setData({ "text" });
    }
    catch (const std::logic_error& e)
    {
        res = true;
    }

    assert(res);
}

void errorDupAttributesAdd()
{
    Tag g{ "g", { { "id", "an_id" } } };

    bool res;
    try
    {
        res = false;
        g.addAttribute({ "id", "other_id" });
    }
    catch (const std::logic_error& e)
    {
        res = true;
    }

    assert(res);
}

void copyAdressCheck()
{
    Tag child{ "rect", { { "width", "10" } }, true };
    Tag parent{ "g", { { "id", "group" } } };
    parent.setData({ child, "text" });

    Tag clone = parent.copy();

    assert(&clone != &parent);
    assert(&clone.getData() != &parent.getData());
    assert(&std::get<Tag>(clone.getData()[0]) != &child);
}

void copyCheckRepr()
{
    Tag child{ "rect", { { "width", "10" } }, true };
    Tag parent{ "g", { { "id", "group" } } };
    parent.setData({ child, "text" });

    Tag clone = parent.copy();

    std::stringstream repr_parent;
    repr_parent << parent;
    std::stringstream repr_clone;
    repr_clone << clone;

    assert(repr_clone.str() == repr_parent.str());
}

void copyProduceIndependantClone()
{
    Tag child{ "rect", { { "width", "10" } }, true };
    Tag parent{ "g", { { "id", "group" } } };
    parent.setData({ child, "text" });

    Tag clone = parent.copy();

    clone.addAttribute({ "class", "copy" });

    std::stringstream repr_parent;
    repr_parent << parent;
    std::stringstream repr_clone;
    repr_clone << clone;

    assert(repr_clone.str() != repr_parent.str());
}

int main(void)
{
    errorDupAttributesInit();
    emptyTag();
    dataEmptyTag();
    errorDupAttributesAdd();
    copyAdressCheck();
    copyCheckRepr();
    copyProduceIndependantClone();
}