#!/opt/homebrew/bin/python3

import os
import sys
import random
import re
import shutil
import subprocess

# global variables
md_blacklist = ["README.md", "CONTRIBUTING.md"]
source_dir = os.path.abspath(sys.argv[1])
target_dir = os.path.join(source_dir, "out")
temp_dir = "/tmp/pandoc_temp" + str(random.random())[2:]
temp_outdir = os.path.join(temp_dir, "out")


def argcheck():
    if len(sys.argv) != 2:
        print("Usage: exporter.py <source_dir>")
        exit()


def exit_procedure():
    print("Deleting temp directory...", end=" ")
    shutil.rmtree(temp_dir)
    print("Done")


def init_procedure():
    # creating both temporary source directory
    # and temporary output directory
    if os.path.exists(temp_dir):
        print("Deleting temp directory...", end=" ")
        shutil.rmtree(temp_dir)
        print("Done")
    print("Creating %s..." % temp_dir)
    os.makedirs(temp_dir)
    print(
        "Creating temporary output directory:\n %s..." % temp_outdir,
        end=" ",
    )
    os.makedirs(temp_outdir)
    print("Done")

    # removing outdated files in final output directory
    choice = input("Removing outdated output files. Do you want to continue? [Y/n]: ")
    if choice is not "Y":
        exit()
    for file in os.listdir(target_dir):
        if file.endswith(".pdf"):
            print("Removing %s" % file)
            os.remove(os.path.join(target_dir, file))


def main():

    # argument check
    argcheck()

    # creating temporary folders
    init_procedure()

    # Copy only ".md" files to temp directory
    # plus the assets folder
    for file in os.listdir(source_dir):
        if file.endswith(".md") and file not in md_blacklist:
            print("Copying %s to temp directory" % file)
            shutil.copy(os.path.join(source_dir, file), temp_dir)
        # we need to copy the assets folder as well
        if file.endswith("assets"):
            print("Copying %s to temp directory" % file)
            shutil.copytree(
                os.path.join(source_dir, file), os.path.join(temp_dir, file)
            )
    print("Done copying source files\n")

    # here we may perform any manipulation to source files

    # Using pandoc to convert source files to .pdf files
    for file in os.listdir(temp_dir):
        if file.endswith(".md"):
            print("Exporting %s to .pdf..." % file, end=" ")
            res = subprocess.check_output(
                [
                    "pandoc",
                    "-s",
                    "--resource-path",
                    temp_dir,
                    "-o",
                    os.path.join(temp_dir, "out", file[:-3] + ".pdf"),
                    os.path.join(temp_dir, file),
                ]
            )
            if res != b"":
                print("\nError exporting %s" % file)
                print(res)
                exit_procedure()
                exit()
            print("Done")
    print("\n")

    # copying files from temporary out directory to target directory
    for file in os.listdir(temp_outdir):
        print("Copying %s to target directory" % file)
        shutil.copy(os.path.join(temp_outdir, file), target_dir)

    print("Check %s directory for output files" % target_dir)
    # Deleting temp directory
    exit_procedure()
    return


if __name__ == "__main__":
    main()
