import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("p", "Hello, world, again!", {})
        self.assertEqual(node.to_html(), "<p>Hello, world, again!</p>")

    def test_leave_to_html_a(self):
        node = LeafNode("a", "Google", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Google</a>')

    def test_leave_to_raw_txt(self):
        node = LeafNode(None, "This is raw!")
        self.assertEqual(node.to_html(), "This is raw!")

    def test_empty_value(self):
        bad_node = LeafNode(None, None)
        self.assertRaises(ValueError, bad_node.to_html)


if __name__ == "__main__":
    unittest.main()
