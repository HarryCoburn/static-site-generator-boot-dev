import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# May not be needed
class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type

    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type.value})"


def block_to_block_type(line):
    if re.match(r"^(#{1,6}) ", line):
        return BlockType.HEADING
    if re.match(r"^```\n[\s\S]*```\Z", line):
        return BlockType.CODE
    if line.startswith(">"):
        return BlockType.QUOTE
    if line.startswith("- "):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\. ", line):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
