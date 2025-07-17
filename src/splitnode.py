from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        parts = text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                # Outside delimiter: keep as TEXT
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Inside delimiter: use the given text_type
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    image_pattern = r'!\[([^\]]+)\]\(([^\)]+)\)'
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(image_pattern, text):
            start, end = match.span()
            alt, url = match.groups()
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = end
        if last_index < len(text):
            after = text[last_index:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    link_pattern = r'(?<!!)(?<!\!)\[([^\]]+)\]\(([^\)]+)\)'
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(link_pattern, text):
            start, end = match.span()
            anchor, url = match.groups()
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            last_index = end
        if last_index < len(text):
            after = text[last_index:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = [n for n in nodes if not (n.text_type == TextType.TEXT and n.text == "")]
    return nodes
