"""
This script propagates changes from source script and configuration
files I want to include in this repository
"""

from hashlib import sha256
from pathlib import Path
from shutil import copy, copytree, make_archive, rmtree
from tempfile import TemporaryDirectory

home = Path.home()

paths = [
    home / ".config" / "fish" / "config.fish",
    home / ".config" / "fish" / "functions" / "fish_prompt.fish",
    home / "bin" / "scripts",
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


def update_path(p):
    subp_num = len(str(p).split("/"))
    for i in range(1, subp_num + 1):
        subp = Path("/".join(str(p).split("/")[:i]))
        if not subp.exists():
            subp.mkdir()


# now we want to copy the files from the paths list to the repo
# only if the hashes are different and by preserving the directory structure
dst_dir = Path(__file__).parent / "conf"
dst_dir.mkdir(exist_ok=True)

for src in paths:
    # we remove the source src_relative prefix in order to
    # preserve the directory structure while copying
    # into the destination directory
    src_relative = src.relative_to(home)
    dst = dst_dir / src_relative

    if src.is_file():
        if not dst.exists() or not compare_file_hashes(src, dst):
            print(f"Copying {src} to {dst}...", end=" ")
            update_path(dst.parent)
            copy(src, dst)
            print("Done")
        else:
            print(f"Skipped {src_relative} because it's already up to date")
    # instead if it's a directory it's a bit more
    # complicated because we need to replicate the precedent
    # behaviour recursively on the contents of the directory

    else:
        if not dst.exists() or not compare_dir_hashes(src, dst):
            print(f"Copying {src} to {dst}...", end=" ")
            # then we copy the source directory content
            # recursively to the destination directory
            rmtree(dst)
            copytree(src, dst)
            print("Done")
        else:
            print(f"Skipped {src_relative} because it's already up to date")
print("Finished! Enjoy your new configuration! :D")
