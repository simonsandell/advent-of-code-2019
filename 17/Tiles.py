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

        self.robot_orientation = 'X'
        self.robot_pos = (-1, -1)
        self.intersections = []
        self.num_intersections = 0

    def build_map(self, ascii_output):
        x = 0
        y = 0
        for char in ascii_output:
            if chr(char) == '\n':
                x = 0
                y += 1
            else:
                self.panels[(x, y)] = chr(char)
                if chr(char) in 'v^<>':
                    self.robot_pos = (x, y)
                    self.robot_orientation = chr(char)
                x += 1

        print('built map')
        print(self)

    def get_color(self, pos):
        if not pos in self.panels:
            return '.'
        return self.panels[pos]


    def find_intersections(self):
        for pos in self.panels:
            if self.panels[pos] != '#':
                continue
            adjacent = Tiles.get_adjacent_positions(pos)
            intersection = True
            for adj in adjacent:
                if self.get_color(adj) != '#':
                    intersection = False
            if intersection:
                if pos not in self.intersections:
                    self.intersections.append(pos)
        self.num_intersections = len(self.intersections)

    def get_sum_of_alignment_parameters(self):
        s = 0
        for intersection in self.intersections:
            s += Tiles.compute_alignment(intersection)
        return s

    def needed_orientation(self, next_pos):
        diff = (self.robot_pos[0] - next_pos[0],
                self.robot_pos[1] - next_pos[1])
        if diff == (0, 1):
            return '^'
        if diff == (0, -1):
            return 'v'
        if diff == (1, 0):
            return '<'
        if diff == (-1, 0):
            return '>'
        raise Exception('Failed to find orientation')

    @staticmethod
    def spin_left(orientation):
        spindict = {'<':'v', 'v':'>', '>':'^', '^':'<'}
        return spindict[orientation]

    def get_spin_moves(self, next_orientation):
        r = []
        while self.robot_orientation != next_orientation:
            r.append('L')
            self.robot_orientation = Tiles.spin_left(self.robot_orientation)
        return r

    def get_robot_move_instruction(self):
        instructions = []
        while True:
            next_pos = self.get_next_pos()
            if next_pos == (-1, -1):
                break
            next_orientation = self.needed_orientation(next_pos)
            if next_orientation != self.robot_orientation:
                instructions.extend(self.get_spin_moves(next_orientation))
            instructions.append(1)
            if self.robot_pos in self.intersections:
                self.intersections.remove(self.robot_pos)
                self.panels[self.robot_pos] = '#'
            else:
                self.panels[self.robot_pos] = '.'
            self.robot_pos = next_pos
            self.panels[self.robot_pos] = self.robot_orientation
            print(self)
        stacked_inst = []
        s = 0
        for inst in instructions:
            if isinstance(inst, int):
                s += inst
            else:
                stacked_inst.append(s)
                s = 0
                stacked_inst.append(inst)
        stacked_inst.append(s)
        while True:
            try:
                stacked_inst.remove(0)
            except ValueError:
                break
        s = ''
        for m in stacked_inst:
            s += str(m)
        s = s.replace('LLL', 'R')
        i = 0
        moves = []
        while i < len(s):
            if s[i] in 'LR':
                moves.append(s[i])
                i += 1
            else:
                if i + 1 < len(s):
                    if s[i+1] not in 'LR':
                        moves.append(int(s[i:i+2]))
                        i += 2
                    else:
                        moves.append(int(s[i]))
                        i += 1
                else:
                    moves.append(int(s[i]))
                    i += 1
        return moves

    def get_straight_move(self):
        if self.robot_orientation == '>':
            return (self.robot_pos[0] + 1, self.robot_pos[1])
        if self.robot_orientation == '<':
            return (self.robot_pos[0] - 1, self.robot_pos[1])
        if self.robot_orientation == 'v':
            return (self.robot_pos[0], self.robot_pos[1] + 1)
        if self.robot_orientation == '^':
            return (self.robot_pos[0], self.robot_pos[1] - 1)
        raise Exception('orientation invalid')

    def get_next_pos(self):
        move_straight = self.get_straight_move()
        if self.get_color(move_straight) == '#':
            return move_straight
        adjacent = Tiles.get_adjacent_positions(self.robot_pos)
        for adj in adjacent:
            if self.get_color(adj) == '#':
                return adj
        return (-1, -1)

    @staticmethod
    def compute_alignment(pos):
        return pos[0]*pos[1]
    @staticmethod
    def get_adjacent_positions(pos):
        return [
            (pos[0]+1, pos[1]),
            (pos[0]-1, pos[1]),
            (pos[0], pos[1]+1),
            (pos[0], pos[1]-1),
            ]

    def __str__(self):
        #time.sleep(0.01)
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
                    out += self.panels[(x, y)]
                else:
                    out += purple
            out += "\n"
        out += "Number of intersections: " + str(self.num_intersections)


        return out
