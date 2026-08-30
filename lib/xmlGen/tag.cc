#include "tag.hh"

#include <set>
#include <sstream>
#include <stdexcept>

Tag::Tag(const std::string& name, const std::vector<attr_t>& attributes,
         bool isEmpty)
    : name_{ name }
    , attributes_{ attributes }
    , isEmpty_{ isEmpty }
{
    std::set<std::string> set;
    for (const auto& [attrName, _] : attributes)
    {
        if (set.contains(attrName))
        {
            throw std::logic_error(
                "Tag: Tag: all attributes must be unique (triggered by:\""
                + attrName + "\")");
        }

        set.insert(attrName);
    }
}

const std::vector<data_t>& Tag::getData() const
{
    return data_;
}

bool Tag::hasAttribute_(attr_t attr) const
{
    const auto& [refName, _] = attr;
    for (const auto& [attrName, _] : attributes_)
    {
        if (refName == attrName)
        {
            return true;
        }
    }

    return false;
}

bool Tag::hasAttribute_(const std::string& refName) const
{
    for (const auto& [attrName, _] : attributes_)
    {
        if (refName == attrName)
        {
            return true;
        }
    }

    return false;
}

std::optional<std::string>
Tag::getAttributeValue_(const std::string& attrName) const
{
    for (const auto& [name, attrVal] : attributes_)
    {
        if (name == attrName)
        {
            return attrVal;
        }
    }

    return std::nullopt;
}

void Tag::addAttribute(attr_t attr)
{
    if (hasAttribute_(attr))
    {
        throw std::logic_error(
            "Tag: addAttribute: Attributes should be unique!");
    }

    attributes_.push_back(attr);
}

void Tag::setData(const std::vector<data_t>& data)
{
    if (isEmpty_)
    {
        throw std::logic_error(
            "Tag: setData: This tag was not meant to recieve any data!");
    }

    data_ = data;
}

Tag Tag::copy() const
{
    return *this;
}

std::ostream& operator<<(std::ostream& os, const std::vector<attr_t>& attrs)
{
    bool isFirst = true;
    for (const auto& [attrName, attrValue] : attrs)
    {
        os << (isFirst ? "" : " ");
        os << attrName << "=" << '"' << attrValue << '"';
        isFirst = false;
    }

    return os;
}

std::ostream& operator<<(std::ostream& os, const std::vector<data_t>& data)
{
    bool isFirst = true;
    for (const auto& child : data)
    {
        if (!isFirst)
        {
            os << "\n";
        }
        else
        {
            isFirst = false;
        }

        if (std::holds_alternative<std::string>(child))
        {
            os << std::get<std::string>(child);
        }
        else if (std::holds_alternative<Tag>(child))
        {
            os << std::get<Tag>(child);
        }
    }

    return os;
}

std::string indent(const std::string& data)
{
    std::stringstream indented;

    bool isLineStart = true;
    for (char c : data)
    {
        if (isLineStart)
        {
            indented << INDENT;
            isLineStart = false;
        }

        indented << c;

        if (c == '\n')
        {
            isLineStart = true;
        }
    }

    return indented.str();
}

void Tag::print_(std::ostream& os) const
{
    os << "<" << name_;

    if (attributes_.size() > 0)
    {
        os << " ";
        os << attributes_;
    }

    if (isEmpty_)
    {
        os << "/>";
        return;
    }

    os << ">\n";
    if (data_.size() > 0)
    {
        std::stringstream data;
        data << data_;

        os << indent(data.str());
        os << "\n";
    }
    os << "</" << name_ << ">";
}

const std::string& Tag::getName() const
{
    return name_;
}

std::ostream& operator<<(std::ostream& os, const Tag& tag)
{
    tag.print_(os);
    return os;
}