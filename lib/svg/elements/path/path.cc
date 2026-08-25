#include "path.hh"

Path::Path(const std::string &path,
           std::optional<Outline> outer)
    : Element{"path", {{"d", path}}, std::nullopt, outer, true}
{
}