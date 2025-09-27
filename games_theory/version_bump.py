import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Bump version (bump) or return actual version (version)?')
        exit(1)
    with open('games_theory/__init__.py', 'r') as file:
        version = file.readline().split('=')[1].strip().strip('"')
        rel_version = version.split('.')
    if sys.argv[1] == 'bump':
        rel_version[2] = str(int(rel_version[2]) + 1)
        bumped_version = '.'.join(rel_version)
        with open('games_theory/__init__.py', 'w') as file:
            file.write('__version__ = "' + bumped_version + '"')
    if sys.argv[1] == 'version':
        sys.stdout.write(version)
        sys.stdout.flush()
