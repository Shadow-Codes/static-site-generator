import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("My name is Shadow", TextType.NORMAL)
        node2 = TextNode("My name is Shadow_Codes", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_empty_text_and_url(self):
        node = TextNode("", TextType.NORMAL, "")
        node2 = TextNode("", TextType.NORMAL, "")
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("My name is Shadow", TextType.NORMAL)
        node2 = TextNode("My name is Shadow", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode(
            "Link to my github", TextType.LINK, "https://github.com/Shadow-Codes"
        )
        node2 = TextNode(
            "Link to my github",
            TextType.LINK,
            None,
        )
        self.assertNotEqual(node, node2)

    def test_special_character(self):
        node = TextNode("!@#$%", TextType.LINK)
        node2 = TextNode("!@#$%", TextType.LINK)
        self.assertEqual(node, node2)

    def test_different_type(self):
        node = TextNode("", TextType.NORMAL)
        self.assertNotEqual(node, "")
        self.assertNotEqual(node, ["", TextType.NORMAL])
        self.assertNotEqual(node, 69420)


if __name__ == "__main__":
    unittest.main()
