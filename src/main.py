import re

from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from node_func import markdown_to_blocks
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"url": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Text node has no corresponding TextType.")


def markdown_to_html_node(document):
    blocks = markdown_to_blocks(document)
    node_list = []

    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        node_list.append(node)

    return node_list


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return HTMLNode("p", block)
        case BlockType.HEADING:
            match = re.match(r"^(#{1,6}) ", block)
            level = len(match.group(1))
            return HTMLNode(
                f"h{level}", block[level + 1 :]
            )  # This should get the space
        case BlockType.QUOTE:
            return HTMLNode("blockquote", block)
        case BlockType.UNORDERED_LIST:
            return HTMLNode("ul", block)
        case BlockType.ORDERED_LIST:
            return HTMLNode("ol", block)
        case BlockType.CODE:
            return HTMLNode("pre", block)

        case _:
            raise ValueError("block_to_html_node received unknown BlockType")


def main():
    document = """\
Paragraph *with some inline* _text stuff_

### Heading 3

> A quote

- unordered list 1
- unordered list 2

1. Item 1
2. Item 2

```
Code code code
```



"""
    print(markdown_to_html_node(document))


main()
