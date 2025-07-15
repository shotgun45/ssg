import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="a", value="link", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertTrue(result.startswith(' '))

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        rep = repr(node)
        self.assertIn("HTMLNode", rep)
        self.assertIn("p", rep)
        self.assertIn("Hello", rep)
        self.assertIn("class", rep)

if __name__ == "__main__":
    unittest.main()
