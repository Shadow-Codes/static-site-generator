import os
import shutil
import sys

from generator import generate_page, generate_pages_recursive
from textnode import TextNode, TextType


def copy_static(source, destination):
    # checking if destination exists before deleting
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # create new destination directory
    os.mkdir(destination)

    for file in os.listdir(source):
        source_file = os.path.join(source, file)
        destination_file = os.path.join(destination, file)

        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
            print(f"{source_file} copied to {destination_file}")
        else:
            copy_static(source_file, destination_file)


def main():
    if len(sys.argv) < 2:
        base_path = "/"
    else:
        base_path = sys.argv[1]
    copy_static("static", "docs")
    generate_pages_recursive(base_path, "content", "template.html", "docs")

    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
