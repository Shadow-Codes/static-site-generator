from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag element is missing")

        if self.children is None:
            raise ValueError("children element(s) is missing")

        # Begin opening tag
        full_tag = f"<{self.tag}"

        # Add attributes if props exist
        if self.props:
            for key, value in self.props.items():
                full_tag += f' {key}="{value}"'

        full_tag += ">"  # Close the opening tag

        # Add child HTML recursively
        for child in self.children:
            full_tag += child.to_html()

        # Add closing tag
        full_tag += f"</{self.tag}>"

        return full_tag
