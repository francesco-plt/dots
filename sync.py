"""
This script propagates changes from source script and configuration
files I want to include in this repository
"""

from hashlib import sha256
from pathlib import Path
from rich.console import Console
from shutil import copy, copytree, make_archive, rmtree
from tempfile import TemporaryDirectory
from colored_traceback import add_hook

home = Path.home()

# why not
add_hook()
console = Console()

paths = [
    home / ".config" / "fish" / "config.fish",
    home / ".config" / "fish" / "functions" / "fish_prompt.fish",
    home / "bin" / "scripts",
    home / "Library" / "Application Support" / "Code" / "User" / "settings.json",
    home / "Library" / "Application Support" / "Firefox" / "Profiles" / "q1iodtvn.default-release" / "chrome"
]


def compare_file_hashes(path1, path2):
    with path1.open("rb") as f1, path2.open("rb") as f2:
        return sha256(f1.read()).hexdigest() == sha256(f2.read()).hexdigest()


def compare_dir_hashes(path1, path2):
    with TemporaryDirectory() as tmpdir:
        # we compress both directories to the temporary directory
        # and we compare the hashes of the compressed files
        make_archive(Path(tmpdir) / "path1", "zip", path1)
        make_archive(Path(tmpdir) / "path2", "zip", path2)
        return compare_file_hashes(
            Path(tmpdir) / "path1.zip", Path(tmpdir) / "path2.zip"
        )


"""
This function takes in a path as input and creates any 
ub-directories that are needed to reach that path. It then
creates a Path object that represents the requested path, and creates
a variable subp_num that represents the number of sub-directories
that are in the path. It then creates a for loop that iterates
through the sub-directories and creates a variable subp that
represents the sub-directory. For every sub-directory that
doesn't exist, it creates it.
"""


def update_path(p):
    subp_num = len(str(p).split("/"))
    for i in range(1, subp_num + 1):
        subp = Path("/".join(str(p).split("/")[:i]))
        if not subp.exists():
            subp.mkdir()


# now we want to copy the files from the paths list to the repo
# only if the hashes are different. We also need to preserve the
# directory structure
dst_dir = Path(__file__).parent / "conf"
dst_dir.mkdir(exist_ok=True)

# if the destination directory is not empty we need to
# remove all the files and directories inside it
if len(list(dst_dir.iterdir())) > 0:
    with console.status("[red]Removing old files..."):
        rmtree(dst_dir)

for src in paths:
    src_relative = src.relative_to(home)
    dst = dst_dir / src_relative

    if src.is_file():
        if not dst.exists() or not compare_file_hashes(src, dst):
            console.print(f"Copying [bold cyan]{src} [default]to [bold cyan]{dst}...", end=" ")
            update_path(dst.parent)
            copy(src, dst)
            console.print("[green]Done")
        else:
            console.print(f"Skipped {src_relative} because it's already up to date")

    # instead if it's a directory it's a bit more
    # complicated because we need to replicate the precedent
    # behaviour recursively on the contents of the directory
    else:
        if not dst.exists() or not compare_dir_hashes(src, dst):
            console.print(f"Copying [bold cyan]{src} [default]to [bold cyan]{dst}...", end=" ")
            # then we copy the source directory content
            # recursively to the destination directory
            if dst.exists():
                rmtree(dst)
            copytree(src, dst)
            console.print("[green]Done")
        else:
            console.print(f"Skipped {src_relative} because it's already up to date")

console.print("[green]Finished! Enjoy your new configuration! :D")
