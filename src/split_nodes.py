from textnode import TextNode, TextType

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
