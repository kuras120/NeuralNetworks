import json
import os
import sys
from pathlib import Path
import shutil
from importlib import resources


class Resource:
    @staticmethod
    def log(path: str):
        print('State saved in path={}'.format(path), file=sys.stderr)

    @staticmethod
    def load(resource_name: str, file_mode: str, base_dir: str):
        base = base_dir + "/data"
        needs_dir = any(ch in file_mode for ch in ('w', 'a', '+'))
        if needs_dir:
            os.makedirs(base, exist_ok=True)
        return open(
            file=os.path.join(base, resource_name),
            mode=file_mode,
            encoding='utf-8'
        )

    @staticmethod
    def copy_defaults(target_dir: str=".", overwrite:bool=False):
        target_root = Path(target_dir)
        dest = target_root / "data"
        base = resources.files("games_theory.resources") / "data"
        with resources.as_file(base) as src_dir:
            for root, _, files in os.walk(src_dir):
                print("Root={}, Files={}".format(root, files), file=sys.stderr)
                rel_root = Path(root).relative_to(src_dir)
                dest_root = dest / rel_root
                dest_root.mkdir(parents=True, exist_ok=True)
                for name in files:
                    src_path = os.path.join(root, name)
                    dst_path = dest_root / name
                    if not dst_path.exists() or overwrite:
                        shutil.copy2(src_path, dst_path)

        Resource.generate_internal_files(str(target_root))

        print("Defaults copied to directory={}".format(dest.resolve()), file=sys.stderr)

    @staticmethod
    def generate_internal_files(resource_path: str="."):
        with Resource.load('config.json', 'r', resource_path) as config_file:
            config = json.load(config_file)
            board_size = config['board-size']
            state = ''.join(['N'] * (board_size * board_size))
            with Resource.load('qtable.json', 'w', resource_path) as q_table_file:
                q_table_weights = [[0] * board_size] * board_size
                q_table = {state: q_table_weights}
                json.dump(q_table, q_table_file)
                Resource.log(q_table_file.name)
            with Resource.load('state.json', 'w', resource_path) as state_file:
                json.dump({'state': state, 'points': ['0', '0']}, state_file)
                Resource.log(state_file.name)


def cli_copy_defaults():
    """
    CLI init entry point for games-theory.

    Usage:
        games-theory-init [path] [--overwrite] [--generate-internals]
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="games-theory-init",
        description="Copy default games_theory config files to a target directory."
    )
    parser.add_argument("path", nargs="?", default=".", help="Destination directory (default: current directory)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files if present")
    parser.add_argument("--generate-internals", action="store_true", help="Generate internal games_theory files (qtable.json, state.json) based on config.json in the target directory")
    args = parser.parse_args()

    if args.generate_internals:
        Resource.generate_internal_files(args.path)
    else:
        Resource.copy_defaults(args.path, overwrite=args.overwrite)
