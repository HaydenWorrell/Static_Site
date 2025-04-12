from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, text_type):
    new_nodes = []
    delimiter_map = {
        TextType.CODE: "`",
        TextType.ITALIC: "_",
        TextType.BOLD: "**",
    }

    delimiter = delimiter_map.get(text_type, "")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            raise ValueError(f"Delimiter not present in node: {node.__repr__()}")

        if node.text.count(delimiter) != 2:
            raise ValueError(f"Delimiter only present once in node: {node.__repr__()}")

        original_text = node.text
        text_list = original_text.split(delimiter, 2)

        before = text_list[0]
        between = text_list[1]
        after = None

        if len(text_list) >= 3:

            after = text_list[2]

        new_nodes.append(TextNode(before, TextType.TEXT))
        new_nodes.append(TextNode(between, text_type))

        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes
