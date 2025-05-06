import unittest

from block import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


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

    def test_paragraph_markdown_to_html(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_markdown_to_html(self):
        md = """
# Heading1
## Heading2
#####Heading5
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading1</h1><h2>Heading2</h2><h5>Heading5</h5></div>",
        )

    def test_code_markdown_to_html(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote_markdown_to_html(self):
        # for quote to be counted as two different quotes they should have blankline between them
        md = """
> First quote
>This should be part of the SAME quote as the first line

>Second quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>First quote This should be part of the SAME quote as the first line</blockquote><blockquote>Second quote</blockquote></div>",
        )

    def test_unordered_markdown_to_html(self):
        md = """
- first item
- second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li></ul></div>",
        )

    def test_ordered_markdown_to_html(self):
        md = """
1. first item
2. second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
