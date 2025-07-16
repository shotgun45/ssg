import unittest
from src.markdownblock import markdown_to_blocks, block_to_block_type

class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("This is a single block."), ["This is a single block."])

    def test_multiple_blocks(self):
        markdown = "First block.\n\nSecond block.\n\nThird block."
        expected = ["First block.", "Second block.", "Third block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_blocks(self):
        markdown = "Block one.\n\n\nBlock two.\n\nBlock three."
        expected = ["Block one.", "Block two.", "Block three."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_whitespace(self):
        markdown = "  Leading whitespace.\n\nTrailing whitespace.  "
        expected = ["Leading whitespace.", "Trailing whitespace."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_consecutive_newlines(self):
        markdown = "Block one.\n\n\n\nBlock two."
        expected = ["Block one.", "Block two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)    

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block).name, "heading")
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block).name, "heading")
        block = "####### Not heading"
        self.assertEqual(block_to_block_type(block).name, "paragraph")

    def test_block_to_block_type_code(self):
        block = """```
code here
```"""
        self.assertEqual(block_to_block_type(block).name, "code")
        block = "```single line code```"
        self.assertEqual(block_to_block_type(block).name, "code")

    def test_block_to_block_type_quote(self):
        block = "> this is a quote\n> another quote"
        self.assertEqual(block_to_block_type(block).name, "quote")
        block = "> only one line"
        self.assertEqual(block_to_block_type(block).name, "quote")

    def test_block_to_block_type_quote_multiline(self):
        block = "> This is a quote.\n> This is still a quote.\n> Another quote line."
        self.assertEqual(block_to_block_type(block).name, "quote")

    def test_block_to_block_type_quote_singleline(self):
        block = "> Single line quote."
        self.assertEqual(block_to_block_type(block).name, "quote")

    def test_block_to_block_type_not_quote(self):
        block = "> This is a quote.\nNot a quote."
        self.assertNotEqual(block_to_block_type(block).name, "quote")

    def test_block_to_block_type_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block).name, "unordered_list")
        block = "- only one"
        self.assertEqual(block_to_block_type(block).name, "unordered_list")

    def test_block_to_block_type_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block).name, "ordered_list")
        block = "1. only one"
        self.assertEqual(block_to_block_type(block).name, "ordered_list")
        block = "1. first\n3. not incremented"
        self.assertEqual(block_to_block_type(block).name, "paragraph")

    def test_block_to_block_type_paragraph(self):
        block = "Just a normal paragraph."
        self.assertEqual(block_to_block_type(block).name, "paragraph")
        block = "Not a list\nNor a heading"
        self.assertEqual(block_to_block_type(block).name, "paragraph")
    
    def test_block_to_block_type_empty(self):
        block = ""
        self.assertEqual(block_to_block_type(block).name, "paragraph")

    def test_block_to_block_type_mixed(self):
        heading_block = "# Heading"
        self.assertEqual(block_to_block_type(heading_block).name, "heading")
        paragraph_block = "This is a paragraph."
        self.assertEqual(block_to_block_type(paragraph_block).name, "paragraph")
        unordered_list_block = "- List item 1\n- List item 2"
        self.assertEqual(block_to_block_type(unordered_list_block).name, "unordered_list")
        code_block = """```python\nprint('Hello')\n```"""
        self.assertEqual(block_to_block_type(code_block).name, "code")
        quote_block = "> Quote here"
        self.assertEqual(block_to_block_type(quote_block).name, "quote")
        ordered_list_block = "1. Ordered item"
        self.assertEqual(block_to_block_type(ordered_list_block).name, "ordered_list")

if __name__ == "__main__":
    unittest.main()