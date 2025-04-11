import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image_link(self):
        node = TextNode(
            "Boots smiling",
            TextType.IMAGE_LINK,
            "https://blog.boot.dev/news/introducing-boots-ai-code-explainer",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://blog.boot.dev/news/introducing-boots-ai-code-explainer",
                "alt": "Boots smiling",
            },
        )


if __name__ == "__main__":
    unittest.main()
