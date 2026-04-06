import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        count = node.text.count(delimiter)
        if count % 2 != 0:
            raise ValueError(
                f"Node text {node.text} lacks closing delimiter {delimiter}"
            )
        sub_node_list = []
        split_text_list = node.text.split(delimiter)
        is_text = True
        for item in split_text_list:
            if is_text is True:
                is_text = False
                if item != "":
                    sub_node_list.append(TextNode(item, TextType.TEXT))
                else:
                    continue
            else:
                sub_node_list.append(TextNode(item, text_type))
                is_text = True
        new_nodes.extend(sub_node_list)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if " ![" not in node.text:
            new_nodes.append(node)
            continue

        split_text_list = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        sub_node_list = []
        for item in split_text_list:
            if item.startswith("!["):
                match = extract_markdown_images(item)[0]
                alt, url = match
                sub_node_list.append(TextNode(alt, TextType.IMAGE, url))
            elif item != "":
                sub_node_list.append(TextNode(item, TextType.TEXT))
        new_nodes.extend(sub_node_list)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if "](" not in node.text:
            new_nodes.append(node)
            continue

        split_text_list = re.split(r"((?<!!)\[.*?\]\(.*?\))", node.text)
        sub_node_list = []

        for item in split_text_list:
            if "](" in item and "![" not in item:
                match = extract_markdown_links(item)[0]
                text, url = match
                sub_node_list.append(TextNode(text, TextType.LINK, url))
            elif item != "":
                sub_node_list.append(TextNode(item, TextType.TEXT))
        new_nodes.extend(sub_node_list)
    return new_nodes


def text_to_textnodes(text):
    base_nodes = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
    )
    base_nodes = split_nodes_delimiter(base_nodes, "`", TextType.CODE)
    base_nodes = split_nodes_delimiter(base_nodes, "_", TextType.ITALIC)
    base_nodes = split_nodes_image(split_nodes_link(base_nodes))

    return base_nodes


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    for idx, line in enumerate(lines):
        lines[idx] = line.strip()
    clean_lines = list(filter(lambda x: x != "", lines))
    return clean_lines


# md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
# """

# print(markdown_to_blocks(md))
