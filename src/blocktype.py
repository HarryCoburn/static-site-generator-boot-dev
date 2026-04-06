import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(line):
    """Takes a block of Markdown line and determines the type"""
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
