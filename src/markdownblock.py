from enum import Enum
import re

BlockType = Enum("BlockType", ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"])

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n")]
    result_blocks = []
    heading_pattern = re.compile(r"^(#{1,6}) .*")
    for block in blocks:
        lines = block.split("\n")
        temp = []
        for line in lines:
            if heading_pattern.match(line):
                if temp:
                    result_blocks.append("\n".join(temp).strip())
                    temp = []
                result_blocks.append(line.strip())
            else:
                temp.append(line)
        if temp:
            result_blocks.append("\n".join(temp).strip())
            
    return [b for b in result_blocks if b]

def block_to_block_type(block):
    lines = block.split("\n")
    if lines[0].startswith("#"):
        if re.match(r"^#{1,6} ", lines[0]):
            return BlockType.heading
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.code
    if all(line.startswith(">") for line in lines):
        return BlockType.quote
    if all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list
    is_ordered = True
    for idx, line in enumerate(lines):
        if not line.startswith(f"{idx+1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ordered_list

    return BlockType.paragraph

