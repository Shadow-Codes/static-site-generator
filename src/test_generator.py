import unittest

from generator import extract_title


class TestGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Heading 1
Normal text
### Heading 3
"""
        result = extract_title(md)
        self.assertEqual(result, "Heading 1")

    def test_extract_title_without_heading(self):
        md = "normal text"
        with self.assertRaises(Exception) as context:
            extract_title(md)

        self.assertEqual(str(context.exception), "No title header found")
