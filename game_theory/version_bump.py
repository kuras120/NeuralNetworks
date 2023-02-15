import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Bump version (bump) or return actual version (version)?')
        exit(1)
    with open('game_theory/release', 'r') as file:
        version = file.read().split('-')
        rel_version = version[0].split('.')
    if sys.argv[1] == 'bump':
        with open('game_theory/release', 'w') as file:
            rel_version[2] = str(int(rel_version[2]) + 1)
            file.write('.'.join(rel_version) + '-SNAPSHOT')
    if sys.argv[1] == 'version':
        sys.stdout.write(version[0])
        sys.stdout.flush()
