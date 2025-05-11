import os
import shutil

from generator import generate_page
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
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
