import Intcode

class Surface:
    def __init__(self):
        self.panels = {}

    def get_color(self, pos):
        if pos in self.panels:
            return self.panels[pos]
        self.panels[pos] = 0
        return 0

    def set_color(self, pos, color):
        self.panels[pos] = color

    def __str__(self):
        blockchar = '█'
        black = '\033[90m' + blockchar + '\033[0m'
        white = '\033[98m' + blockchar + '\033[0m'
        transp = ' '

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
        out = ''
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                if (x, y) in self.panels:
                    if self.get_color((x, y)) == 0:
                        out += black
                    else:
                        out += white
                else:
                    out += transp
            out += "\n"
        return out

class Robot:
    def __init__(self):
        self.orientations = {0:'^', 1:'>', 2:'v', 3:'<'}
        self.orientation = 0
        self.position = (0, 0)

        self.surface = Surface()

        self.output_toggle = False

    def rotate(self, right):
        if right:
            self.orientation = (self.orientation + 1) % 4
            return
        if self.orientation:
            self.orientation -= 1
        else:
            self.orientation = 3

    def move(self):
        dx = 0
        dy = 0
        if self.orientation == 0:
            dy = 1
        if self.orientation == 1:
            dx = 1
        if self.orientation == 2:
            dy = -1
        if self.orientation == 3:
            dx = -1
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def paint(self, color):
        self.surface.set_color(self.position, color)

    def camera(self):
        return self.surface.get_color(self.position)

    def output_handle(self, val):
        if not self.output_toggle:
            self.paint(val)
            self.output_toggle = not self.output_toggle
            return
        self.rotate(val)
        self.move()
        self.output_toggle = not self.output_toggle

if __name__ == '__main__':
    with open('input', 'r') as f:
        program = f.read().split(',')
    PROG = [int(x) for x in program]
    COMP = Intcode.Intcode()
    COMP.memory = PROG
    COMP.increase_memory(10)
    ROB = Robot()
    ROB.surface.set_color((0, 0), 1)
    COMP.input_method = ROB.camera
    COMP.output_method = ROB.output_handle
    COMP.run()
    print(ROB.surface)
    print(len(ROB.surface.panels))
