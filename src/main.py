from textnode import TextNode, TextType


def main():
    new_node = TextNode("Here is a URL", TextType.LINK, "https://www.boot.dev")
    print(new_node)


main()
