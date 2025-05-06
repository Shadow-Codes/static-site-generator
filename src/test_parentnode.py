import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren_and_great_grandchildren(self):
        great_grandchild_node_1 = LeafNode("b", "great_grandchild_1")
        great_grandchild_node_2 = LeafNode("p", "great_grandchild_2")
        grandchild_node_1 = ParentNode("b", [LeafNode(None, "grandchild1")])
        grandchild_node_2 = ParentNode(
            "li", [great_grandchild_node_1, great_grandchild_node_2]
        )
        child_node = ParentNode("li", [grandchild_node_1, grandchild_node_2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><li><b>grandchild1</b><li><b>great_grandchild_1</b><p>great_grandchild_2</p></li></li></div>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()

        self.assertEqual(str(context.exception), "children element(s) is missing")


if __name__ == "__main__":
    unittest.main()
