import re
from shlex import split

from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from node_func import markdown_to_blocks, text_to_textnodes
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

        if block_type != BlockType.CODE:
            node = text_to_children(node, block_type)
        else:
            child_text_node = TextNode(node.value[4:-3], TextType.CODE)
            child_node = text_node_to_html_node(child_text_node)
            node = ParentNode(node.tag, [child_node])
        node_list.append(node)
    node_tree = ParentNode("div", node_list)
    return node_tree


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
            return HTMLNode("blockquote", block[1:].strip())
        case BlockType.UNORDERED_LIST:
            return HTMLNode("ul", block)
        case BlockType.ORDERED_LIST:
            return HTMLNode("ol", block)
        case BlockType.CODE:
            return HTMLNode("pre", block)
        case _:
            raise ValueError("block_to_html_node received unknown BlockType")


def text_to_children(node, block_type):
    if (
        block_type == BlockType.PARAGRAPH
        or block_type == BlockType.HEADING
        or block_type == BlockType.QUOTE
    ):
        text = node.value.replace("\n", " ")
        sub_nodes = text_to_textnodes(text)
        leaf_nodes = []
        for sub_node in sub_nodes:
            leaf_nodes.append(text_node_to_html_node(sub_node))
        return ParentNode(node.tag, leaf_nodes)
    elif block_type == BlockType.UNORDERED_LIST:
        split_text = node.value.split("\n")
        leaf_nodes = []
        for text in split_text:
            text = text[2:]
            sub_nodes = text_to_textnodes(text)
            sub_leaf_nodes = []
            for sub_node in sub_nodes:
                sub_leaf_nodes.append(text_node_to_html_node(sub_node))
            ordered_list_item = ParentNode("li", sub_leaf_nodes)
            leaf_nodes.append(ordered_list_item)
        return ParentNode(node.tag, leaf_nodes)
    elif block_type == BlockType.ORDERED_LIST:
        split_text = node.value.split("\n")
        leaf_nodes = []
        for text in split_text:
            text = text[text.index(" ") + 1 :]
            sub_nodes = text_to_textnodes(text)
            sub_leaf_nodes = []
            for sub_node in sub_nodes:
                sub_leaf_nodes.append(text_node_to_html_node(sub_node))
            ordered_list_item = ParentNode("li", sub_leaf_nodes)
            leaf_nodes.append(ordered_list_item)
        return ParentNode(node.tag, leaf_nodes)


def main():
    document = """\
This is a
Paragraph **with some inline** _text stuff_

### This is a Heading 3 level

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
    md = markdown_to_html_node(document)
    print(md.to_html())


main()
