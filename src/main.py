from htmlnode import LeafNode
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
    print(blocks)


def main():
    document = """\
Paragraph

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
