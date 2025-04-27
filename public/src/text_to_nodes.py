from split_nodes import split_nodes_link, split_nodes_delimiter, split_nodes_image
from textnode import TextNode, TextType


def text_to_textnodes(text, delimiter_types=None):
    if delimiter_types is None:
        # Start with all delimiter types in a specific order
        delimiter_types = [TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.IMAGE, TextType.LINK]
    
    # Base case: no more delimiter types to process
    if not delimiter_types:
        return [TextNode(text, TextType.TEXT)]
    
    # Process the first delimiter type
    current_type = delimiter_types[0]
    remaining_types = delimiter_types[1:]
    
    # Create initial node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process based on delimiter type
    if current_type in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        nodes = split_nodes_delimiter(nodes, current_type)
    elif current_type == TextType.IMAGE:
        nodes = split_nodes_image(nodes)
    elif current_type == TextType.LINK:
        nodes = split_nodes_link(nodes)
    
    # Recursively process remaining delimiter types for each node
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT and remaining_types:
            # Only process TEXT nodes for remaining delimiters
            result.extend(text_to_textnodes(node.text, remaining_types))
        else:
            result.append(node)
    
    return result