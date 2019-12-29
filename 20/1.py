import Tiles


if __name__ == '__main__':
    maze = Tiles.Tiles()
    with open('input', 'r') as f:
        i = f.read().split('\n')
    for y, line in enumerate(i):
        for x, char in enumerate(line):
            maze.set_color((x, y), char)

    maze.find_portals()
    print(maze.portals['AY'])
    print(len(maze.extra_adjacent))
    steps = maze.walk(maze.startpos, maze.endpos)
    print(maze)
    print('steps', steps)
