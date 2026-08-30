#include <cassert>
#include <iostream>

#include "../elements/shapes/text.hh"
#include "../svg.hh"

int main(void)
{
    Tspan t2{};
    t2.setData({ "nested" });
    Text t1{};
    t1.setData({ "hello", t2 });
    SVG valid{ 100, 100 };
    valid.setData({ t1 });

    SVG invalid1{ 100, 100 };
    invalid1.setData({ Tspan{} });

    Tspan t3{};
    t3.setData({ "inner" });
    SVG invalid2{ 100, 100 };
    invalid2.setData({ "wrong", t3 });

    assert(valid.checkTspan());
    assert(!invalid1.checkTspan());
    assert(!invalid2.checkTspan());

    try
    {
        std::cout << invalid1;
        assert(false);
    }
    catch (const std::logic_error& e)
    {
        assert(std::string{ e.what() }
               == "SVG: print_: Tspan instances must be children of other "
                  "Tspan or Text instances!");
    }
}