import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Click me",
            props={
                "href": "https://www.boot.dev",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev" target="_blank">Click me</a>',
        )

    """
    self.assertRaises(ValueError) passes when we call code and it raises an exception.
    In this case because self.value is None it will raise ValueError because I have 
    if statement which checks if self.value in None in leafnode.py 
    """

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Value string")
        self.assertEqual(node.to_html(), "Value string")
