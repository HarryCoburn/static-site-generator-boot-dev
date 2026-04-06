class HTMLNode:
    """Base Class for HTML nodes"""

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag  # string reprenting HTML tag name. None renders raw text.
        self.value = value  # Value of the html tag. None assumes tag has children
        self.children = (
            children  # List of HTMLNode child objects. None assumes self.value != None
        )
        self.props = props  # Dict of attributes of self.tag (e.g. {"href": "https://google.com"})

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):  # TODO: Prop sanitation
        html_string = ""
        if self.props is None or self.props == {}:
            return html_string
        for prop in self.props:
            html_string += f' {prop}="{self.props[prop]}"'
        return html_string

    def __repr__(self):
        return f"HTMLNode: (Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Properties: {self.props}"


class LeafNode(HTMLNode):
    """Represents a leaf in the HTML tree. Must have a value and no children."""

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value  # raw text
        if self.props is None or self.props == {}:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (
            f"LeafNode: (Tag: {self.tag}, Value: {self.value}, Properties: {self.props}"
        )


class ParentNode(HTMLNode):
    """Represents a parent node in the HTML tree. Must have children and no value."""

    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode has no tag.")
        if self.children is None or self.children == {}:
            raise ValueError("ParentNode has no children.")
        html_str = f"<{self.tag}>"
        for child in self.children:
            html_str += child.to_html()
        return html_str + f"</{self.tag}>"
