import time
blockchar = '█'
clearscreen = '\033[2J'
transparent = ' '
red = '\033[31m' + blockchar + '\033[0m' # red
lgreen = '\033[32m' + blockchar + '\033[0m' # light green
yellow = '\033[33m' + blockchar + '\033[0m' # yellow
lblue = '\033[34m' + blockchar + '\033[0m' # light blue
magenta = '\033[35m' + blockchar + '\033[0m' # magenta
cyan = '\033[36m' + blockchar + '\033[0m' # cyan
orange = '\033[91m' + blockchar + '\033[0m' # orange
dgrey = '\033[92m' + blockchar + '\033[0m' # dark grey
grey = '\033[93m' + blockchar + '\033[0m' # grey
lgrey = '\033[94m' + blockchar + '\033[0m' # light grey
purple = '\033[95m' + blockchar + '\033[0m' # purple
llgrey = '\033[96m' + blockchar + '\033[0m' # ligher grey

class Tiles:
    def __init__(self):
        self.panels = {}

        self.keys = {}
        self.keys_rev = {}
        self.doors = {}
        self.player = None

        self.held_keys = []
        self.adj_cache = {}

        self.covered = []
        self.edges = 0
        self.steps = 0


    def set_color(self, pos, color):
        if str.isalpha(color) and str.isupper(color):
            self.doors[color] = pos
        if str.isalpha(color) and str.islower(color):
            self.keys[color] = pos
            self.keys_rev[pos] = color
        if color == '@':
            self.player = pos

        self.panels[pos] = color

    def get_color(self, pos):
        if not pos in self.panels:
            return '#'
        return self.panels[pos]

    @staticmethod
    def encode_keys(held_keys):
        return "".join(sorted(held_keys))


    def lock_door(self, door):
        self.set_color(self.doors[door], door)

    def unlock_door(self, door):
        self.set_color(self.doors[door], '.')

    def swipe_key(self, key):
        self.set_color(self.keys[key], '.')

    def place_key(self, key):
        self.set_color(self.keys[key], key)
    def update_doors(self, held_keys):
        self.held_keys = held_keys
        for door in self.doors:
            if door.lower() in self.held_keys:
                self.unlock_door(door)
            else:
                self.lock_door(door)
        for key in self.keys:
            if key in self.held_keys:
                self.swipe_key(key)
            else:
                self.place_key(key)

    @staticmethod
    def get_adjacent_positions(pos):
        return [
            (pos[0]+1, pos[1]),
            (pos[0]-1, pos[1]),
            (pos[0], pos[1]+1),
            (pos[0], pos[1]-1),
            ]

    def __str__(self, player=None):
        time.sleep(0.01)
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0
        for pos in self.panels:
            if pos[0] > max_x:
                max_x = pos[0]
            if pos[0] < min_x:
                min_x = pos[0]
            if pos[1] > max_y:
                max_y = pos[1]
            if pos[1] < min_y:
                min_y = pos[1]
        out = clearscreen
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in self.panels:
                    if (x, y) in self.covered:
                        out += lgreen
                    else:
                        out += self.panels[(x, y)]
                else:
                    out += purple
            out += "\n"
        out += "Edges: " + str(self.edges) + '\n'
        out += "Steps: " + str(self.steps) + '\n'

        return out
    def get_adjacent_keys(self, start, held_keys):
        self.update_doors(held_keys)

        state = (start, self.encode_keys(held_keys))
        if state in self.adj_cache:
            return self.adj_cache[state]

        steps = 0
        edges = Tiles.get_adjacent_positions(start)
        visited = set(start)
        keys = {}
        while True:
            self.covered = visited
            steps += 1
            next_edges = []
            for e in edges:
                visited.add(e)
                if str.islower(self.get_color(e)):
                    if e not in keys:
                        keys[e] = steps
                if self.get_color(e) != '#' and not str.isupper(self.get_color(e)):
                    ne = Tiles.get_adjacent_positions(e)
                    for pe in ne:
                        c = self.get_color(pe)
                        if c != '#' and not str.isupper(c) and pe not in visited:
                            next_edges.append(pe)
            edges = next_edges
            self.edges = len(edges)
            self.steps = steps
            if len(edges) == 0:
                break
        self.adj_cache[state] = keys    
        return keys
