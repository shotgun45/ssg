import unittest
from src.markdownblock import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()