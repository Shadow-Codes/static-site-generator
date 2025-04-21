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
