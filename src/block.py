def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")

    filtered_markdown = list(
        filter(lambda split: split, map(lambda split: split.strip(), split_markdown))
    )

    return filtered_markdown
