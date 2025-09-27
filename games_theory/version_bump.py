import sys
from games_theory import __version__

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Bump version (bump) or return actual version (version)?')
        exit(1)
    rel_version = __version__.split('.')
    if sys.argv[1] == 'bump':
        rel_version[2] = str(int(rel_version[2]) + 1)
        __version__ = '.'.join(rel_version)
    if sys.argv[1] == 'version':
        sys.stdout.write(__version__)
        sys.stdout.flush()
