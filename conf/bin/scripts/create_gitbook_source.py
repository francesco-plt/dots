#!/opt/homebrew/bin/python3

"""
Francesco Pallotta 2022
The purpose of this script is to take a list of files and for
each of them, to manipulate its content and to copy into a
predefined folder which will be used later on as source for a
Gitbook space. Then we want to create a ".gitbook.yaml"configuration
file. In particular we want to modify input files by:
1. replacing occurrences of single dollar character inline latex with double dollar
2. replacing occurrences of images path (of the type "assets/xxx.png") with "../assets/xxx.png"
As for the ".gitbook.yaml" file, we want to create it with the following content:
"root: ./src/gitbook/"

Note also that the script assumes that the markdown files are in a folder called "src"
"""

from argparse import ArgumentParser
from pathlib import Path
from re import compile, sub


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="path to the repository which you want to publish",
        required=True,
    )
    args = parser.parse_args()

    input_folder = Path(args.input)
    output_folder = Path(args.input) / "src/gitbook"

    if (
        not input_folder.exists()
        or not (input_folder / "src").exists()
        or not any((input_folder / "src").iterdir())
    ):
        print("The input folder does not exist or it is empty. Exiting...")
        exit(1)

    # Create output folder if it does not exist
    if not output_folder.exists():
        print("Creating output folder...", end=" ")
        output_folder.mkdir(parents=True)
        print("Done")
    else:
        print("Output folder already exists. Updating its content...")

    # Create ".gitbook.yaml" file
    gitbook_yaml_file = input_folder / ".gitbook.yaml"
    if not gitbook_yaml_file.exists():
        with gitbook_yaml_file.open("w") as f:
            f.write("root: ./src/gitbook/")

    # creating SUMMARY.md file if it does not exist
    summary_file = output_folder / "SUMMARY.md"
    if not summary_file.exists():
        with summary_file.open("w") as f:
            f.write("# Table of contents\n\n")

    # editing files
    for file in (input_folder / "src").glob("*.md"):

        with file.open("r") as f:
            content = f.read()

        if (output_folder / file.name).exists():
            with (output_folder / file.name).open("r") as f:
                old_content = f.read()
                if old_content == content:
                    print(f"Skipping {file.name} because it's unchanged...")
                    continue

        # replace single dollar character with double dollar but only
        # if it is not followed or preceded by another dollar symbol

        """
        chatgpt is saying:
        the negative lookahead (?!\$) ensures that the dollar sign is not
        followed by another dollar sign, and the negative lookbehind (?<!\$)
        ensures that the dollar sign is not preceded by another dollar sign. 
        """
        r1 = compile(r"(?<!\$)\$(?!\$)")
        content = r1.sub("$$", content)

        # replace images path (hopefully I did not wrote aything else
        # which contains "assets/")
        content = content.replace("assets/", "../assets/")

        # write new content into output file
        output_file = output_folder / file.name
        with output_file.open("w") as f:
            print(f"Writing {file.name}...", end=" ")
            f.write(content)
            print("Done")

        print("Updating reference in SUMMARY.md...", end=" ")
        with summary_file.open("a") as f:
            f.write(f"* [{file.stem}]({file.name})\n")
        print("Done")

    print("Done. Enjoy your Gitbook!")


if __name__ == "__main__":
    main()
