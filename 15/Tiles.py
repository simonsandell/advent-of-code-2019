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

class Hallway:
    tile_to_color = {
        0:"D", # droid
        1:"#",       # wall
        2:purple,      # unknown
        3:".",      # empty hallway
        4:orange       # win
        }

    def __init__(self):
        self.panels = {}
        self.steps = {(0,0):0}
        self.stepcount = 0

        self.oxygen = (-1, -1)

        self.oxygen_edge = []

    def get_adjacent_positions(self, pos):
        return [
                (pos[0]+1, pos[1]),
                (pos[0]-1, pos[1]),
                (pos[0], pos[1]+1),
                (pos[0], pos[1]-1),
                ]


    def get_adjacent_hallways(self, pos):
        adj = self.get_adjacent_positions(pos)
        r = []
        for a in adj:
            c = self.get_color(a)
            if c == 3:
                r.append(a)
        return r

        



    def get_color(self, pos):
        if pos in self.panels:
            return self.panels[pos]
        self.panels[pos] = 2
        return 2

    def get_step(self, pos):
        return self.steps[pos]

    def set_color(self, pos, color, paint=False):
        prev_color = self.get_color(pos)
        self.panels[pos] = color
        if color == 0:
            self.stepcount += 1
            if prev_color == 2:
                self.steps[pos] = self.stepcount
            if prev_color == 3:
                self.stepcount = self.steps[pos]
        if color == 4:
            self.oxygen = pos
            self.stepcount += 1
            self.steps[pos] = self.stepcount
        if paint:
            print(self)
            time.sleep(0.05)



    def __str__(self):
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
        for y in range(min_y, max_y + 1, 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in self.panels:
                    out += Hallway.tile_to_color[self.get_color((x, y))]
                else:
                    out += purple
            out += "\n"
        out += "Steps: " + str(self.stepcount)

        return out
