import unittest
from src.markdown import markdown_to_html_node, text_to_children, extract_title

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# Heading 1
## Heading 2
### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First
2. Second
3. Third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_quote(self):
        md = "> This is a quote\n> with two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith two lines</blockquote></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Heading

Paragraph text.

- List item 1
- List item 2

> Quote here

```
code block
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>Paragraph text.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>Quote here</blockquote><pre><code>code block\n</code></pre></div>",
        )

class TestTextToChildren(unittest.TestCase):
    def test_text_to_children_plain(self):
        children = text_to_children("plain text")
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].tag, None)
        self.assertEqual(children[0].value, "plain text")

    def test_text_to_children_bold(self):
        children = text_to_children("This is **bold** text.")
        self.assertEqual(len(children), 3)
        self.assertEqual(children[1].tag, "b")
        self.assertEqual(children[1].value, "bold")

    def test_text_to_children_italic(self):
        children = text_to_children("This is _italic_ text.")
        self.assertEqual(len(children), 3)
        self.assertEqual(children[1].tag, "i")
        self.assertEqual(children[1].value, "italic")

    def test_text_to_children_code(self):
        children = text_to_children("Here is `code`.")
        self.assertEqual(len(children), 3)
        self.assertEqual(children[1].tag, "code")
        self.assertEqual(children[1].value, "code")

    def test_text_to_children_link(self):
        children = text_to_children("A [link](https://example.com)")
        self.assertEqual(len(children), 2)
        self.assertEqual(children[1].tag, "a")
        self.assertEqual(children[1].value, "link")
        self.assertEqual(children[1].props["href"], "https://example.com")

    def test_text_to_children_image(self):
        children = text_to_children("An image ![alt](url)")
        self.assertEqual(len(children), 2)
        self.assertEqual(children[1].tag, "img")
        self.assertEqual(children[1].props["src"], "url")
        self.assertEqual(children[1].props["alt"], "alt")

    def test_text_to_children_mixed(self):
        children = text_to_children("**bold** and _italic_ and `code` and [link](url) and ![img](imgurl)")
        tags = [c.tag for c in children]
        self.assertIn("b", tags)
        self.assertIn("i", tags)
        self.assertIn("code", tags)
        self.assertIn("a", tags)
        self.assertIn("img", tags)

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Title\nSome content"
        title = extract_title(md)
        self.assertEqual(title, "Title")

    def test_extract_title_no_header(self):
        md = "No title here"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("No h1 header found in markdown." in str(context.exception))

    def test_extract_title_leading_whitespace(self):
        md = "   #   My Title   "
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    def test_extract_title_multiple_headers(self):
        md = "# First\n# Second\nContent"
        title = extract_title(md)
        self.assertEqual(title, "First")

    def test_extract_title_h2_not_h1(self):
        md = "## Not a title\n# Real Title"
        title = extract_title(md)
        self.assertEqual(title, "Real Title")

    def test_extract_title_h1_with_extra_hashes(self):
        md = "# Title #\nContent"
        title = extract_title(md)
        self.assertEqual(title, "Title #")

    def test_extract_title_h1_with_only_hash(self):
        md = "#   "
        title = extract_title(md)
        self.assertEqual(title, "")

if __name__ == "__main__":
    unittest.main()