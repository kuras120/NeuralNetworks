import os
import sys


class Resource:
    @staticmethod
    def log(path):
        print('State saved in ' + path, file=sys.stderr)

    @staticmethod
    def load(resource_name: str, file_mode: str):
        return open(
            file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', resource_name),
            mode=file_mode,
            encoding='utf-8'
        )
