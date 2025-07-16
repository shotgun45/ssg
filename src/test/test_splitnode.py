import unittest
from src.textnode import TextNode, TextType
from src.splitnode import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("A `b` c `d` e", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No code here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("No code here", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_non_text_nodes(self):
        node = TextNode("Bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_multiple_images(self):
        node = TextNode("![one](url1) and ![two](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode("No images here!", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_image_at_start_and_end(self):
        node = TextNode("![start](url1) middle ![end](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_image_with_text_only(self):
        node = TextNode("Just text, no images.", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode("This is a [link](https://example.com) in text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode("[one](url1) and [two](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("one", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode("No links here!", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_link_at_start_and_end(self):
        node = TextNode("[start](url1) middle [end](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url2"),
        ]
        self.assertEqual(result[0].text, "start")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[1].text, " middle ")
        self.assertEqual(result[2].text, "end")
        self.assertEqual(result[2].text_type, TextType.LINK)

    def test_link_with_image_in_text(self):
        node = TextNode("[link](url) and ![img](imgurl)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result[0].text, "link")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[1].text, " and ![img](imgurl)")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_link_with_text_only(self):
        node = TextNode("Just text, no links.", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is a simple text."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is a simple text.", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_with_code(self):
        text = "Here is some `inline code`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is some ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_bold(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_italic(self):
        text = "This is _italic_ text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_image(self):
        text = "Here is an ![alt](url) image."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" image.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_link(self):
        text = "Go to [site](url)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("site", TextType.LINK, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_all_features(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_nested_features(self):
        text = "**bold and _italic_**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold and _italic_", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_multiple_features(self):
        text = "**bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)

    def test_text_with_no_features(self):
        text = "plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("plain text", TextType.TEXT)]
        self.assertEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()
