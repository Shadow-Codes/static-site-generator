from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")
        if self.tag is None:
            return self.value

        # For tags without attributes
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        full_tag = f"<{self.tag}"
        # For tags with attributes
        for key, value in self.props.items():
            full_tag += f' {key}="{value}"'
        full_tag += f">{self.value}</{self.tag}>"

        return full_tag
