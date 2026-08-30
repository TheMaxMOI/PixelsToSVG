#include "comment.hh"

std::ostream& comment(std::ostream& os, const std::string& string)
{
    return os << "<!-- " << string << "-->";
}