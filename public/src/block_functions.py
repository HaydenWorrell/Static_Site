from block_types import BlockType
import re


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks if block != ""]
    final_blocks = []

    for block in stripped_blocks:
        if "\n" in block:
            split_block = block.split("\n")
            repaired_list = []

            for s_block in split_block:
                s_block = s_block.strip()
                repaired_list.append(s_block)

            repaired_block = "\n".join(repaired_list)

            block = repaired_block

        final_blocks.append(block)

    return final_blocks


def block_to_block_type(block):
    if re.match(r"^(#{1,6})\s(.*)", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith("> "):
        return BlockType.QUOTE

    if block.startswith("- "):
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        lines = block.split("\n")
        expected_number = 1

        for line in lines:
            match = re.match(r"^(\d+)\.\s+.*", line)
            if match:
                number = int(match.group(1))
                if number != expected_number:
                    return BlockType.PARAGRAPH
                expected_number += 1
            else:
                return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH
