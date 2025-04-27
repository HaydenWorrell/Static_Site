from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links


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
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) != 2:
            new_nodes.append(node)
            continue

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


def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_images(node.text)

        if not images:
            result.append(node)
            continue

        current_text = node.text

        while images:
            image_alt, image_url = images[0]

            parts = current_text.split(f"![{image_alt}]({image_url})", 1)

            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(image_alt, TextType.IMAGE, image_url))
            current_text = parts[1]
            images = extract_markdown_images(current_text)

        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            result.append(node)
            continue

        current_text = node.text

        while links:
            link_alt, link_url = links[0]

            parts = current_text.split(f"[{link_alt}]({link_url})", 1)

            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(link_alt, TextType.LINK, link_url))
            current_text = parts[1]
            links = extract_markdown_links(current_text)

        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result
