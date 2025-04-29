import unittest

from block import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
