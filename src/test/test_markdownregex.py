import unittest
from src.markdownregex import extract_markdown_images, extract_markdown_links

class TestMarkdownRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "![one](url1) and ![two](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("one", "url1"),
            ("two", "url2"),
        ], matches)

    def test_no_images(self):
        text = "No images here!"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_multiple_links(self):
        text = "[one](url1) and [two](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("one", "url1"),
            ("two", "url2"),
        ], matches)

    def test_no_links(self):
        text = "No links here!"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_images_not_links(self):
        text = "![notalink](url)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_links_and_images(self):
        text = "[link](url1) and ![img](url2)"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertListEqual([("link", "url1")], links)
        self.assertListEqual([("img", "url2")], images)

if __name__ == "__main__":
    unittest.main()