import json
import os
import sys
from pathlib import Path
import shutil
from importlib import resources


class Resource:
    DATA_DIR = 'data'

    @staticmethod
    def load(resource_name: str, file_mode: str, base_dir: str):
        base = Path(base_dir) / Resource.DATA_DIR
        needs_dir = any(ch in file_mode for ch in ('w', 'a', '+'))
        if needs_dir:
            os.makedirs(base, exist_ok=True)
        return open(
            file=base / resource_name,
            mode=file_mode,
            encoding='utf-8'
        )

    @staticmethod
    def save(resource_name: str, key: str, value: any, base_dir: str):
        data = {}
        try:
            with Resource.load(resource_name, 'r', base_dir) as f:
                data = json.load(f)
        except FileNotFoundError:
            pass

        data[key] = value

        with Resource.load(resource_name, 'w', base_dir) as f:
            json.dump(data, f)
            print('Value saved in file - key={},value={},file={}'.format(key, value, f.name), file=sys.stderr)

    @staticmethod
    def copy_defaults(source_package: str= "games_theory.resources", target_dir: str= ".", overwrite:bool=False):
        target_root = Path(target_dir)
        dest = target_root / Resource.DATA_DIR
        base = resources.files(source_package) / Resource.DATA_DIR
        config_file_found = False
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
                    if name == 'config.json':
                        config_file_found = True

        if not config_file_found:
            raise FileNotFoundError("config.json not found in resources")

        Resource.save('config.json', 'resource_path', str(target_root), str(target_root))
        Resource.generate_internal_files(str(target_root))

        print("Defaults copied to directory={}".format(dest.resolve()), file=sys.stderr)

    @staticmethod
    def generate_internal_files(resource_path: str="."):
        with Resource.load('config.json', 'r', resource_path) as config_file:
            config = json.load(config_file)
            board_size = config['board-size']
            state = ''.join(['N'] * (board_size * board_size))

            q_table_weights = [[0] * board_size] * board_size
            Resource.save('qtable.json', state, q_table_weights, resource_path)

            Resource.save('state.json', 'state', state, resource_path)
            Resource.save('state.json', 'points', ['0', '0'], resource_path)


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
        Resource.copy_defaults(target_dir=args.path, overwrite=args.overwrite)
