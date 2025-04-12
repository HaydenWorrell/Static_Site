from textnode import TextNode, TextType


def main():
    test_node = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")

    print(test_node.__repr__())


if __name__ == "__main__":
    main()
