#pragma once

#include <tuple>
#include <ostream>
#include <string>
#include <vector>
#include <variant>

#define INDENT "    "

class Tag;

using attr_t = std::tuple<std::string, std::string>;
using data_t = std::variant<std::string, Tag>;

template <typename TagFunc>
concept Callable = requires(TagFunc f, Tag &tag) {
    f(tag);
};

class Tag
{
private:
    std::string name_;
    std::vector<attr_t> attributes_;
    std::vector<data_t> data_;
    bool isEmpty_;

    bool hasAttribute_(attr_t attr) const;

public:
    Tag(const std::string &name,
        const std::vector<attr_t> &attributes = {},
        bool isEmpty = false);

    virtual ~Tag() = default;

    void addAttribute(attr_t attr);
    void setData(const std::vector<data_t> &data);
    virtual Tag copy() const;

    template <Callable TagFunc>
    void visit(TagFunc f) const; // could be replaced with a visitor

    friend std::ostream &operator<<(std::ostream &os, const Tag &tag); // could be replaced with a visitor
};

std::ostream &operator<<(std::ostream &os, const std::vector<attr_t> &attrs);
std::ostream &operator<<(std::ostream &os, const std::vector<data_t> &data);

#include "tag.hxx"