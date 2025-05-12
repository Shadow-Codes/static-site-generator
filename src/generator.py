import os
from os.path import isfile

from block import markdown_to_html_node


def extract_title(markdown):
    headers = list(filter(lambda line: line.startswith("# "), markdown.split("\n")))
    if not headers:
        raise Exception("No title header found")
    return headers[0][2:].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = open(from_path, "r").read()
    temp = open(template_path, "r").read()

    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    final_html = temp.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    dir_path = os.path.dirname(dest_path)

    # checking if destination exists before deleting
    if not os.path.exists(dir_path):
        # create new destination directory
        os.makedirs(dir_path)

    f = open(dest_path, "w")
    f.write(final_html)
    f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    names = os.listdir(dir_path_content)

    for name in names:
        full_path = os.path.join(dir_path_content, name)

        if os.path.isfile(full_path):
            filename, ext = os.path.splitext(name)
            new_file_name = filename + ".html"
            dest_file = os.path.join(dest_dir_path, new_file_name)
            generate_page(full_path, template_path, dest_file)
        else:
            updated_dest_dir_path = os.path.join(dest_dir_path, name)
            os.makedirs(updated_dest_dir_path, exist_ok=True)
            generate_pages_recursive(full_path, template_path, updated_dest_dir_path)
