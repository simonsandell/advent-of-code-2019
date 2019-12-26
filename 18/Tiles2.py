import time
import itertools
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
        self.doors_rev = {}
        self.robot_starts = []

        self.robot_positions = []

        self.key_to_door = {}
        self.door_to_key = {}

        self.adj_cache = {}

        self.keys_to_robots = {}
        self.doors_to_robots = {}

        self.robot_to_doors = {}
        self.robot_to_keys = {}

        self.weight_cache = {}

        self.key_to_needed_keys = {}

        self.color = set()

    def assign_door_to_key(self):
        for letter, pos in self.keys.items():
            for dletter, dpos in self.doors.items():
                if letter == dletter.lower():
                    self.door_to_key[dpos] = pos
                    self.key_to_door[pos] = dpos

    def get_closest_robot(self, pos):
        mindist = 9999999
        minrob = None
        for robot in self.robot_starts:
            d = (abs(robot[0] - pos[0]) + abs(robot[1] - pos[1]))
            if  d < mindist:
                mindist = d
                minrob = robot
        return minrob

    def find_needed_keys(self, key):
        robot = self.get_closest_robot(key)
        doors = self.robot_to_doors[robot]
        potentially_needed_keys = [self.door_to_key[x] for x in doors]
        adj_keys = self.get_adjacent_keys(robot, set())
        if key in adj_keys:
            return set()
        r = 1
        allbutkey = set(self.keys.values())
        allbutkey.remove(key)

        while r <= len(potentially_needed_keys):
            for c in itertools.combinations(potentially_needed_keys, r):
                adj_keys = self.get_adjacent_keys(robot, set(c))
                if key in adj_keys:
                    return set(c)
            r += 1
        raise Exception("Couldn't get key")

    def assign_needed_keys(self):
        for key in self.keys.values():
            self.key_to_needed_keys[key] = self.find_needed_keys(key)


    def assign_to_robots(self):
        for key in self.keys.values():
            rob = self.get_closest_robot(key)
            self.keys_to_robots[key] = rob
            self.robot_to_keys[rob].append(key)
        for door in self.doors.values():
            rob = self.get_closest_robot(door)
            self.doors_to_robots[door] = rob
            self.robot_to_doors[rob].append(door)

    def set_color(self, pos, color):
        if str.isalpha(color) and str.isupper(color):
            self.doors[color] = pos
            self.doors_rev[pos] = color
        if str.isalpha(color) and str.islower(color):
            self.keys[color] = pos
            self.keys_rev[pos] = color
        if color == '@':
            self.robot_starts.append(pos)
            self.robot_positions.append(pos)
            self.robot_to_doors[pos] = []
            self.robot_to_keys[pos] = []

        self.panels[pos] = color

    def get_color(self, pos):
        if not pos in self.panels:
            return '#'
        return self.panels[pos]

    def encode_keys(self, held_keys):
        r = []
        for k in held_keys:
            r.append(self.keys_rev[k])
        return "".join(sorted(r))

    def update_doors(self, held_keys):
        all_doors = list(self.doors.values())
        for door in all_doors:
            req_key = self.door_to_key[door]
            if req_key in held_keys:
                self.set_color(door, '.')
            else:
                self.set_color(door, self.doors_rev[door])
        for keypos in self.keys.values():
            if keypos in held_keys:
                self.set_color(keypos, '.')
            else:
                self.set_color(keypos, self.keys_rev[keypos])

    def open_doors(self):
        all_doors = list(self.doors.values())
        for door in all_doors:
            self.set_color(door, '.')
        for key in self.keys:
            self.set_color(self.keys[key], key)

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
                if (x, y) in self.color:
                    out += orange
                elif (x, y) in self.panels:
                    out += self.panels[(x, y)]
                else:
                    out += purple
            out += "\n"

        return out

    @staticmethod
    def get_pair_state(fr, to):
        l = sorted((fr, to))
        s = (l[0][0], l[0][1], l[1][0], l[1][1])
        return s

    def get_steps_between(self, fr, to):
        s = Tiles.get_pair_state(fr, to)
        if s in self.weight_cache:
            return self.weight_cache[s]
        adj = self.get_adjacent_keys(fr, set(), no_doors=True)
        for k, w in adj.items():
            ks = Tiles.get_pair_state(fr, k)
            self.weight_cache[ks] = w
        if not s in self.weight_cache:
            print(self)
            print('fr', fr, 'to', to)
            print('to', self.keys_rev[to])
            raise Exception('could find steps between')
        return self.weight_cache[s]

    def clear_robot_symbols(self):
        for rpos in self.robot_starts:
            self.set_color(rpos, '.')


    def get_nn_weights(self, start, held_keys):
        closest_robot = self.get_closest_robot(start)
        keys_in_area = self.robot_to_keys[closest_robot]
        available_keys = set()
        for k in keys_in_area:
            if k not in held_keys:
                needed_keys = self.key_to_needed_keys[k]
                if needed_keys.issubset(held_keys):
                    available_keys.add(k)
        nn = {}
        for ak in available_keys:
            s = Tiles.get_pair_state(start, ak)
            if s not in self.weight_cache:
                nn[ak] = self.get_steps_between(start, ak)
            else:
                nn[ak] = self.weight_cache[s]
        return nn

    def get_adjacent_keys(self, start, held_keys, no_doors=False):
        if no_doors:
            self.open_doors()
        else:
            self.update_doors(held_keys)
        state = (start, self.encode_keys(held_keys))
        if state in self.adj_cache:
            return self.adj_cache[state]
        steps = 0
        edges = Tiles.get_adjacent_positions(start)
        visited = set(start)
        keys = {}
        while True:
            steps += 1
            next_edges = []
            for e in edges:
                visited.add(e)
                if str.islower(self.get_color(e)):
                    if e not in keys:
                        keys[e] = steps
                    self.set_color(e, '.')
                if self.get_color(e) != '#' and not str.isupper(self.get_color(e)):
                    ne = Tiles.get_adjacent_positions(e)
                    for pe in ne:
                        c = self.get_color(pe)
                        if c != '#' and not str.isupper(c) and pe not in visited:
                            next_edges.append(pe)
            edges = next_edges[:]
            if len(edges) == 0:
                break
        self.adj_cache[state] = keys
        self.color = visited
        return keys
