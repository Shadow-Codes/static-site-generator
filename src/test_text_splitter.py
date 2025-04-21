import unittest

from text_splitter import split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()
