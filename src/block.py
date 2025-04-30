from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")

    filtered_markdown = list(
        filter(lambda split: split, map(lambda split: split.strip(), split_markdown))
    )

    return filtered_markdown


def block_to_block_type(text):
    lines = text.split("\n")
    count = 0

    # Heading check
    while count < len(text) and text[count] == "#":
        count += 1
    if 1 <= count <= 6 and count < len(text) and text[count] == " ":
        return BlockType.HEADING

    # Code check
    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    # Quote check
    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE

    # Unordered list check
    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDERED_LIST

    # Ordered list check
    current_line_number = 1

    for line in lines:
        if not line.startswith(f"{current_line_number}. "):
            break
        current_line_number += 1
    else:
        return BlockType.ORDERED_LIST

    """
    If the text is not any of the type above it is paragraph by default
    according to assignment.
    """
    return BlockType.PARAGRAPH
