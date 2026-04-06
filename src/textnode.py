from enum import Enum


class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"


class TextNode:
    """Information node for inline tags"""

    def __init__(self, text, text_type, url=None) -> None:
        self.text = text  # The text content of the node
        self.text_type = text_type  # the TextType of the node
        self.url = url  # URL of link or image, or None

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
