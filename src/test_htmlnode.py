import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")


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

    def test_to_html_multiple_children(self):
        children = [LeafNode("b", "Bold"), LeafNode(None, "Normal"), LeafNode("i", "Italic")]
        parent_node = ParentNode("p", children)
        self.assertEqual(parent_node.to_html(), "<p><b>Bold</b>Normal<i>Italic</i></p>")

    def test_to_html_nested_parents(self):
        inner = ParentNode("span", [LeafNode("b", "deep")])
        outer = ParentNode("div", [inner, LeafNode(None, "text")])
        self.assertEqual(outer.to_html(), "<div><span><b>deep</b></span>text</div>")

    def test_to_html_with_props(self):
        children = [LeafNode("b", "Bold")]
        parent_node = ParentNode("div", children, props={"class": "container", "id": "main"})
        html = parent_node.to_html()
        self.assertIn('<div', html)
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.startswith('<div '))
        self.assertTrue(html.endswith('</div>'))

    def test_to_html_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("h1", "Title"),
                    LeafNode("p", "Paragraph")
                ])
            ])
        ])
        expected = "<div><section><article><h1>Title</h1><p>Paragraph</p></article></section></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_to_html_children_with_none(self):
        with self.assertRaises(AttributeError):
            ParentNode("div", [None]).to_html()

    def test_to_html_raises_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "fail")])

    def test_to_html_raises_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_leaf_to_html_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("a", "Google", {"href": "https://www.google.com", "target": "_blank"})
        html = node.to_html()
        self.assertIn('href="https://www.google.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.startswith('<a '))
        self.assertTrue(html.endswith('>Google</a>'))

if __name__ == "__main__":
    unittest.main()