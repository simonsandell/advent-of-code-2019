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

class GameSurface:
    tile_to_color = {
        0:transparent, # empty
        1:dgrey,       # wall
        2:purple,      # block
        3:lgreen,      # paddle
        4:red          # ball
        }

    def __init__(self):
        self.panels = {}
        self.tilecount = {}
        self.score = 0
        self.ball_pos = 0
        self.paddle_pos = 0

        self.instructions = []
        self.first_input = False

        self.interp = 0

    def get_color(self, pos):
        if pos in self.panels:
            return self.panels[pos]
        self.panels[pos] = 0
        return 0

    def set_color(self, pos, color):
        if color in self.tilecount:
            self.tilecount[color] = self.tilecount[color] + 1
        else:
            self.tilecount[color] = 1
        if color == 3:
            self.paddle_pos = pos[0]
        if color == 4:
            self.ball_pos = pos[0]
        self.panels[pos] = color

    def read_instructions(self, value):
        self.instructions.append(value)
        if len(self.instructions) == 3:
            if self.instructions[0] == -1 and self.instructions[1] == 0:
                self.score = self.instructions[2]
            else:
                self.set_color((self.instructions[0], self.instructions[1]), self.instructions[2])
            self.instructions[:] = []
            self.draw()

    def botplayer(self):
        if not self.first_input:
            self.first_input = True
        if self.ball_pos < self.paddle_pos:
            return -1
        if self.ball_pos > self.paddle_pos:
            return 1
        return 0

    def draw(self):
        if not self.first_input:
            return
        if self.interp % 30 != 0:
            self.interp += 1
            return
        print(self)
        time.sleep(1/60)

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
                    out += GameSurface.tile_to_color[self.get_color((x, y))]
                else:
                    out += transparent
            out += "\n"
        out += "Score: " + str(self.score) + "\n"
        return out
