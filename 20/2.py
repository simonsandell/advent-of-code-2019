import Tiles


if __name__ == '__main__':
    maze = Tiles.Tiles()
    with open('tinput', 'r') as f:
        i = f.read().split('\n')
    for y, line in enumerate(i):
        for x, char in enumerate(line):
            maze.set_color((x, y), char)

    maze.find_portals()
    maze.build_cache()
    f = maze.walk_recursively()
    print(f)

