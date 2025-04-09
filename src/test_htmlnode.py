import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("h1", "title", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode("a", "click me", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "click me",
            props={
                "href": "https://www.boot.dev",
                "target": "_blank",
            },
        )

        # Storing string return in html variable for readablity
        html = node.props_to_html()

        """
        assertIn tests if the text is in html or not
        Works similar to apple in ["apple", "banana"]
        """
        self.assertIn(' href="https://www.boot.dev"', html)
        self.assertIn(' target="_blank"', html)

        """
        This tests number of double quotes.
        It should be 4 because we have two props and each will have starting and ending quotes.
        """
        self.assertEqual(html.count('"'), 4)
        self.assertTrue(html.startswith(" "))  # This tests if string starts with space


if __name__ == "__main__":
    unittest.main()
