import re
from markdownblock import markdown_to_blocks, block_to_block_type, BlockType
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from splitnode import text_to_textnodes

def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.heading:
            import re
            m = re.match(r"^(#{1,6}) ", block)
            level = len(m.group(1)) if m else 1
            tag = f"h{level}"
            text = block[level+1:] if m else block
            node = ParentNode(tag, text_to_children(text))
        elif block_type == BlockType.code:
            lines = block.split("\n")
            if lines[0].startswith("```") and lines[-1].startswith("```") and len(lines) >= 2:
                code_lines = lines[1:-1]
            else:
                code_lines = lines
            code_text = "\n".join(code_lines) + "\n"
            code_node = LeafNode("code", code_text)
            node = ParentNode("pre", [code_node])
        elif block_type == BlockType.quote:
            quote_text = "\n".join([line[2:] if line.startswith("> ") else line[1:] for line in block.split("\n")])
            node = ParentNode("blockquote", text_to_children(quote_text))
        elif block_type == BlockType.unordered_list:
            items = [line[2:] for line in block.split("\n")]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            node = ParentNode("ul", li_nodes)
        elif block_type == BlockType.ordered_list:
            items = [line[line.find(". ")+2:] for line in block.split("\n")]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            node = ParentNode("ol", li_nodes)
        else:
            para_text = " ".join(block.split("\n"))
            node = ParentNode("p", text_to_children(para_text))
        children.append(node)
    return ParentNode("div", children)

def extract_title(markdown):
    for line in markdown.splitlines():
        m = re.match(r"^\s*# (.*)", line)
        if m:
            return m.group(1).strip()
    raise Exception("No h1 header found in markdown.")