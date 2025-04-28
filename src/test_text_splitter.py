import unittest

from text_splitter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("Plain Text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain Text")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_code_delimiter(self):
        node = TextNode("Text with `code block`", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_bold_delimiter(self):
        node = TextNode("Text with **bold text**", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold text")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_italic_delimiter(self):
        node = TextNode("Text with _italic text_", TextType.NORMAL)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "italic text")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_link_delimiter(self):
        node = TextNode(
            "boot.dev website [website](https://boot.dev) and boot.dev youtube [youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot.dev website ", TextType.NORMAL),
                TextNode("website", TextType.LINK, "https://boot.dev"),
                TextNode(" and boot.dev youtube ", TextType.NORMAL),
                TextNode(
                    "youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            result,
        )

    def test_image_delimiter(self):
        node = TextNode(
            "First link ![image](https://i.imgur.com/zjjcJKZ.png) and second link ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First link ", TextType.NORMAL),
                TextNode(
                    "image", TextType.IMAGE_LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and second link ", TextType.NORMAL),
                TextNode(
                    "second image",
                    TextType.IMAGE_LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            result,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE_LINK,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )

    def test_empty_text_to_textnodes(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertListEqual([], result)


if __name__ == "__main__":
    unittest.main()
