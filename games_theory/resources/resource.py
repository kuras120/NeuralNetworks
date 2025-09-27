import os
import sys
from pathlib import Path
import shutil
from importlib import resources


class Resource:
    @staticmethod
    def log(path):
        print('State saved in ' + path, file=sys.stderr)

    @staticmethod
    def load(resource_name: str, file_mode: str, base_dir: str = None):
        """
        Open a resource from user-copied resources.

        Resolution order for base directory:
        1) base_dir argument (if provided)
        2) Current working directory

        Behavior:
        - Read modes open the file from the resolved directory.
        - Write/append modes ensure the directory exists, then open the file there.
        """
        base = (base_dir or os.getcwd()) + "/data"
        needs_dir = any(ch in file_mode for ch in ('w', 'a', '+'))
        if needs_dir:
            os.makedirs(base, exist_ok=True)
        return open(
            file=os.path.join(base, resource_name),
            mode=file_mode,
            encoding='utf-8'
        )

    @staticmethod
    def copy_defaults(target_dir=".", overwrite=False):
        """
        Copy packaged default data files into target_dir.
        - target_dir: directory to place the files (string or Path)
        - overwrite: if False, existing files are preserved
        """
        target_root = Path(target_dir)
        dest = target_root / "data"
        base = resources.files("games_theory.resources") / "data"
        with resources.as_file(base) as src_dir:
            if overwrite:
                # Copy the entire directory and overwrite existing files
                shutil.copytree(src_dir, dest, dirs_exist_ok=True)
            else:
                # Merge without overwriting existing files
                for root, _, files in os.walk(src_dir):
                    print("Root {}, Files {}".format(root, files), file=sys.stderr)
                    rel_root = Path(root).relative_to(src_dir)
                    dest_root = dest / rel_root
                    dest_root.mkdir(parents=True, exist_ok=True)
                    for name in files:
                        src_path = os.path.join(root, name)
                        dst_path = dest_root / name
                        if not dst_path.exists():
                            shutil.copy2(src_path, dst_path)

        print(f"Defaults copied to: {dest.resolve()}", file=sys.stderr)


def cli_copy_defaults():
    """
    Console command:
      games-theory-init [path] [--overwrite] [--use]

    - path: optional destination directory (defaults to current directory)
    - --overwrite: replace existing files if present
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="games-theory-init",
        description="Copy default games_theory config/state files to a target directory."
    )
    parser.add_argument("path", nargs="?", default=".", help="Destination directory (default: current directory)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files if present")
    args = parser.parse_args()

    Resource.copy_defaults(args.path, overwrite=args.overwrite)
