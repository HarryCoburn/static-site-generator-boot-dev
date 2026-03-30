import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_blank_node(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_HTMLnode_repr(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "https://google.com"})
        actual_repr = repr(node)
        expected_repr = "HTMLNode: (Tag: a, Value: Google, Children: None, Properties: {'href': 'https://google.com'}"
        self.assertEqual(actual_repr, expected_repr)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        node.props = {}
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com"})
        prop_str = node.props_to_html()
        self.assertEqual(prop_str, ' href="https://google.com"')
        node.props["target"] = "_blank"
        new_prop_str = node.props_to_html()
        self.assertEqual(new_prop_str, ' href="https://google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()
