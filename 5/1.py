import sys

class Intcode:
    def __init__(self):
        self.OPCODES = {1:self.add, 2:self.multiply, 3:self.save, 4:self.output, 99:self.halt}
        self.memory = []
        self.cursor = 0
        self.modes = 0

    def get_value(self, mode, param):
        # the param indicates the position of the real input
        # position mode
        if mode == 0:
            return self.memory[param]
        # the param is the real input
        # immediate mode
        if mode == 1:
            return param

    def get_mode(self, n):
        return self.modes % pow(10, n) // pow(10, n-1)

    def save(self):
        inp = int(input("INPUT "))
        target_position = self.memory[self.cursor+1]
        self.memory[target_position] = inp
        self.cursor += 2
        return False

    def output(self):
        out = self.get_value(self.get_mode(1), self.memory[self.cursor + 1])
        print("OUTPUT",out)
        self.cursor += 2
        return False

    def add(self):
        # tree parameters, three modes
        term_1 = self.get_value(self.get_mode(1), self.memory[self.cursor + 1])
        term_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        Sum = term_1 + term_2

        target_position = self.memory[self.cursor+3]
        self.memory[target_position] = Sum
        self.cursor += 4
        return False

        
    def multiply(self):
        factor_1 = self.get_value(self.get_mode(1), self.memory[self.cursor + 1])
        factor_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        product = factor_1 * factor_2

        target_position = self.memory[self.cursor+3]
        self.memory[target_position] = product
        self.cursor += 4
        return False

    def halt(self):
        self.cursor += 1
        return True

    def run(self):
        while True:
            opcode = self.memory[self.cursor] % 100
            self.modes = self.memory[self.cursor] // 100
            #print('opcode', opcode)
            if not opcode in self.OPCODES:
                raise ValueError("invalid opcode")
            halt = self.OPCODES[opcode]()
            if halt:
                return False
        return True

if __name__=="__main__":
    mem = []
    with open("./input", "r") as f:
        mem = f.read().split(",")
    mem = [int(x) for x in mem]
    computer = Intcode()
    computer.memory = mem.copy()
    computer.run()
