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

        self.portals = {}
        self.extra_adjacent = {}

        self.startpos = None
        self.endpos = None

        self.visited = set()
        self.steps = 0

    def set_color(self, pos, color):
        self.panels[pos] = color

    def get_color(self, pos):
        if pos in self.panels:
            return self.panels[pos]
        return ' '

    def find_the_hallway(self, positions):
        for pos in positions:
            if self.get_color(pos) == '.':
                return pos
        raise Exception('No hallway found')

    def find_portals(self):
        for pos, char in self.panels.items():
            if char.isupper():
                adj = Tiles.get_adjacent_positions(pos)
                other = None
                for a in adj:
                    c = self.get_color(a)
                    if c.isupper():
                        other = a
                        break
                portal = ''.join(sorted((char, c)))
                if portal not in self.portals:
                    self.portals[portal] = [other, pos]
                else:
                    if pos not in self.portals[portal]:
                        self.portals[portal].append(other)
                        self.portals[portal].append(pos)
        for portal, spanning in self.portals.items():
            if len(spanning) > 3:
                adj = Tiles.get_adjacent_positions(spanning[0])
                adj.extend(Tiles.get_adjacent_positions(spanning[1]))
                a = self.find_the_hallway(adj)

                adj = Tiles.get_adjacent_positions(spanning[2])
                adj.extend(Tiles.get_adjacent_positions(spanning[3]))
                b = self.find_the_hallway(adj)

                self.extra_adjacent[a] = b
                self.extra_adjacent[b] = a
            if portal == 'AA':
                adj = Tiles.get_adjacent_positions(spanning[0])
                adj.extend(Tiles.get_adjacent_positions(spanning[1]))
                self.startpos = self.find_the_hallway(adj)
            if portal == 'ZZ':
                adj = Tiles.get_adjacent_positions(spanning[0])
                adj.extend(Tiles.get_adjacent_positions(spanning[1]))
                self.endpos = self.find_the_hallway(adj)


    @staticmethod
    def get_adjacent_positions(pos):
        return [
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1])
            ]

    def __str__(self):
        #time.sleep(0.01)
        max_x = 0
        max_y = 0
        min_x = 99999999999999999
        min_y = 99999999999999999
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
                if (x, y) in self.visited:
                    out += lblue
                elif (x, y) in self.panels:
                    out += self.panels[(x, y)]
                else:
                    out += purple
            out += '\n'
        out += 'Steps: '  + str(self.steps) + '\n'
        return out

    def get_adjacent_hallways(self, pos):
        r = set()
        if pos in self.extra_adjacent:
            r.add(self.extra_adjacent[pos])

        adj = Tiles.get_adjacent_positions(pos)
        for a in adj:
            if self.get_color(a) == '.':
                r.add(a)
        return r

    def walk(self, fr, to):
        steps = {}
        current_steps = 0
        current_edges = self.get_adjacent_hallways(fr)
        while True:
            next_edges = set()
            current_steps += 1
            for pos in current_edges:
                if pos == to:
                    return current_steps
                pne = self.get_adjacent_hallways(pos)
                for e in pne:
                    if e not in steps:
                        steps[e] = current_steps
                        next_edges.add(e)
            current_edges = next_edges
            if len(current_edges) == 0:
                raise Exception('Didn\'t reach goal')
            self.visited = set(steps.keys())
            self.steps = current_steps
            print(self)
            time.sleep(0.01)
