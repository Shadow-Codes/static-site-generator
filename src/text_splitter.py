import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            list_of_nodes.append(node)
            continue
        if delimiter not in node.text:
            list_of_nodes.append(node)
            continue

        text1, remainder = node.text.split(delimiter, 1)

        if delimiter not in remainder:
            raise Exception(f"No closing delimiter found for {delimiter}")

        inline_text, text2 = remainder.split(delimiter, 1)

        list_of_nodes.append(TextNode(text1, TextType.NORMAL))
        list_of_nodes.append(TextNode(inline_text, text_type))

        if text2:
            list_of_nodes.extend(
                split_nodes_delimiter(
                    [TextNode(text2, TextType.NORMAL)], delimiter, text_type
                )
            )

    return list_of_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    list_of_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            list_of_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            list_of_nodes.append(node)
            continue

        current_text = node.text

        for alt_text, url in links:
            sections = current_text.split(f"[{alt_text}]({url})", 1)

            # sections[0] is text before [alt_text] so this adds it if not empty
            if sections[0]:
                list_of_nodes.append(TextNode(sections[0], TextType.NORMAL))

            list_of_nodes.append(TextNode(alt_text, TextType.LINK, url))

            if len(sections) > 1:
                current_text = sections[1]
            else:
                current_text = ""

        if current_text:
            list_of_nodes.append(TextNode(current_text, TextType.NORMAL))

    return list_of_nodes


def split_nodes_image(old_nodes):
    list_of_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            list_of_nodes.append(node)
            continue

        links = extract_markdown_images(node.text)

        if not links:
            list_of_nodes.append(node)
            continue

        current_text = node.text

        for alt_text, url in links:
            sections = current_text.split(f"![{alt_text}]({url})", 1)

            if sections[0]:
                list_of_nodes.append(TextNode(sections[0], TextType.NORMAL))

            list_of_nodes.append(TextNode(alt_text, TextType.IMAGE_LINK, url))

            if len(sections) > 1:
                current_text = sections[1]
            else:
                current_text = ""

        if current_text:
            list_of_nodes.append(TextNode(current_text, TextType.NORMAL))

    return list_of_nodes


def text_to_textnodes(text):
    list_of_nodes = [TextNode(text, TextType.NORMAL)]
    list_of_nodes = split_nodes_image(list_of_nodes)
    list_of_nodes = split_nodes_link(list_of_nodes)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "**", TextType.BOLD)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "_", TextType.ITALIC)
    list_of_nodes = split_nodes_delimiter(list_of_nodes, "`", TextType.CODE)

    return [node for node in list_of_nodes if node.text]
