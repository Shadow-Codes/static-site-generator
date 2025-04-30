import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_markdown_to_blocks_extra_blanks(self):
        markdown = """
- First list item
- Second list item


There are **two** blank lines above and **one** below this.

"""

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "- First list item\n- Second list item",
                "There are **two** blank lines above and **one** below this.",
            ],
            blocks,
        )

    def test_markdown_to_blocks_empty_output(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual([], blocks)

    def test_block_to_block_type_heading(self):
        text = "##### Heading5"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_near_miss(self):
        text = "###Missing Space After '#'"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_extra_hash(self):
        text = "####### Not valid heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        text = """> First quote
>Second quote"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_near_miss(self):
        text = """
> First quote

>Second quote
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        text = """```
print(hello)
```"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_near_miss(self):
        text = """```
print(hello)
``"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        text = """
- item one
- item two
- item three
""".strip()
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_near_miss(self):
        text = """
- item one
- item two
-item three
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        text = """
1. item one
2. item two
3. item three
""".strip()
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_near_miss(self):
        text = """
1. item one
2. item two
4. item four
""".strip()
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        text = "Lorem Ipsum"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiline(self):
        text = """
First Line
Second Line
Third Line
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_mixed(self):
        text = """
1. ordered
- unordered
# heading
>quote
lorem ipsum
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # Recommended by Boots
    def test_block_to_block_type_heading_inside_code_block(self):
        text = """```
### Heading inside code block
```"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)


if __name__ == "__main__":
    unittest.main()
