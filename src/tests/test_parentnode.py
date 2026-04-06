import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        parent_node = ParentNode(None, {})
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        self.assertEqual("ParentNode has no tag.", str(context.exception))

    def test_no_children(self):
        parent_node = ParentNode("div", {})
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        self.assertEqual("ParentNode has no children.", str(context.exception))

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("b", "bold child")
        parent_node = ParentNode("div", [child_node, child_node_2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child</span><b>bold child</b></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_full(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode("i", "italian grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node_2])
        child_leaf_node = LeafNode("p", "I'm an uncle!")
        parent_node = ParentNode("div", [child_leaf_node, child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>I'm an uncle!</p><span><b>grandchild</b><i>italian grandchild</i></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
