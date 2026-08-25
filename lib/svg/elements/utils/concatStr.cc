#include "concatStr.hh"

#include <sstream>

std::string joinWithSpace(const std::vector<std::string> stringList)
{
    std::stringstream growingString;

    bool isFirst = true;
    for (const auto &str : stringList)
    {
        if (isFirst)
        {
            isFirst = false;
        }
        else
        {
            growingString << ' ';
        }

        growingString << str;
    }

    return growingString.str();
}