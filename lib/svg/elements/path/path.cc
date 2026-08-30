#include "path.hh"

Path::Path(const std::string& path, std::optional<Coloring> inner,
           std::optional<Outline> outer)
    : Element{ "path", { { "d", path } }, inner, outer, true }
{}