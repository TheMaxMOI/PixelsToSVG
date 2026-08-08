import unittest

from xmlGen import Tag


class TestTag(unittest.TestCase):
    def test_duplicate_attributes_raise_value_error(self):
        with self.assertRaises(ValueError):
            Tag("g", [("id", "bottom"), ("id", "left")])

    def test_empty_tag_is_self_closing(self):
        tag = Tag("rect", isEmpty=True)
        self.assertEqual("<rect/>", repr(tag))

    def test_set_data_on_empty_tag_raises_type_error(self):
        tag = Tag("img", isEmpty=True)
        with self.assertRaises(TypeError):
            tag.setData(["text"])

    def test_add_duplicate_attribute_raises_value_error(self):
        tag = Tag("g", [("id", "bottom")])
        with self.assertRaises(ValueError):
            tag.addAttribute(("id", "bottom"))

    def test_repr_of_copy(self):
        child = Tag("rect", [("width", "10")], isEmpty=True)
        parent = Tag("g", [("id", "group")])
        parent.setData([child, "text"])

        clone = parent.copy()

        self.assertIsNot(clone, parent)
        self.assertIsNot(clone.attributes, parent.attributes)
        self.assertIsNot(clone.data, parent.data)
        self.assertIsNot(clone.data[0], child)

        self.assertEqual(repr(parent), repr(clone))

    def test_copy_returns_independent_clone(self):
        child = Tag("rect", [("width", "10")], isEmpty=True)
        parent = Tag("g", [("id", "group")])
        parent.setData([child, "text"])

        clone = parent.copy()

        self.assertIsNot(clone, parent)
        self.assertIsNot(clone.attributes, parent.attributes)
        self.assertIsNot(clone.data, parent.data)
        self.assertIsNot(clone.data[0], child)

        clone.attributes.append(("class", "copy"))
        clone.data[0].addAttribute(("height", "20"))

        self.assertNotIn(("class", "copy"), parent.attributes)
        self.assertNotIn(("height", "20"), child.attributes)
        self.assertEqual(
            '<g id="group">\n    <rect width="10"/>\n    text\n</g>', repr(parent)
        )


if __name__ == "__main__":
    unittest.main()
