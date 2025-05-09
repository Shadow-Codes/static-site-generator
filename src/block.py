from enum import Enum

from parentnode import ParentNode
from text_splitter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


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


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    parent_node = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                block_content = block.replace("\n", " ")
                paragraph_node = ParentNode("p", text_to_children(block_content))
                parent_node.children.append(paragraph_node)

            case BlockType.HEADING:
                lines = block.split("\n")
                for line in lines:
                    if not line.strip():
                        continue

                    count = 0
                    while count < len(line) and line[count] == "#":
                        count += 1

                    if count == 0:
                        continue

                    # handling space after #
                    if count < len(line) and line[count] == " ":
                        heading_text = line[count + 1 :]
                    else:
                        heading_text = line[count:]

                    heading_node = ParentNode(
                        f"h{count}", text_to_children(heading_text)
                    )
                    parent_node.children.append(heading_node)

            case BlockType.CODE:
                lines = block.split("\n")
                # removes ``` at start and end
                code_block_content = "\n".join(lines[1:-1]) + "\n"

                """
                we don't want to process text inside code block.
                if text contains **bold** inside code block it should be kept as it is.
                so no need to use text_to_children() here
                """

                code_text_node = TextNode(code_block_content, TextType.NORMAL)
                code_html_node = text_node_to_html_node(code_text_node)

                code_node = ParentNode("code", [code_html_node])

                """
                The <pre> tag preserves spaces, tabs, and line breaks exactly as they appear
                so we need to wrap our html tag with pre tag like
                <pre><code>...</code></pre>

                Hint given by Boots
                """
                pre_node = ParentNode("pre", [code_node])

                parent_node.children.append(pre_node)

            case BlockType.QUOTE:
                lines = block.split("\n")
                quote_list = []

                for line in lines:
                    if line.startswith("> "):
                        quote_list.append(line[2:])
                    elif line.startswith(">"):
                        quote_list.append(line[1:])

                quote_content = " ".join(quote_list)

                quote_node = ParentNode("blockquote", text_to_children(quote_content))
                parent_node.children.append(quote_node)

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items = []

                for line in lines:
                    item_content = line[2:]
                    item_node = ParentNode("li", text_to_children(item_content))
                    list_items.append(item_node)

                list_node = ParentNode("ul", list_items)

                parent_node.children.append(list_node)

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_items = []

                for line in lines:
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        item_content = parts[1]
                        item_node = ParentNode("li", text_to_children(item_content))
                        list_items.append(item_node)

                list_node = ParentNode("ol", list_items)
                parent_node.children.append(list_node)

            case _:
                raise Exception("Not valid block type")

    return parent_node
