import sys

class Intcode:
    def __init__(self):
        self.OPCODES = {1:self.add, 2:self.multiply, 99:self.halt}
        self.memory = []
        self.cursor = 0

    def add(self):
        subject_1 = self.memory[self.cursor+1]
        subject_2 = self.memory[self.cursor+2]
        target = self.memory[self.cursor+3]
        self.memory[target] = self.memory[subject_1] + self.memory[subject_2]
        self.cursor += 4
        return False


    def multiply(self):
        subject_1 = self.memory[self.cursor+1]
        subject_2 = self.memory[self.cursor+2]
        target = self.memory[self.cursor+3]
        self.memory[target] = self.memory[subject_1] * self.memory[subject_2]
        self.cursor += 4
        return False

    def halt(self):
        self.cursor += 1
        return True

    def run(self):
        while self.memory[self.cursor] in self.OPCODES:
            halt = self.OPCODES[self.memory[self.cursor]]()
            if halt:
                return False
        return True

if __name__=="__main__":
    mem = []
    with open("./input", "r") as f:
        mem = f.read().split(",")
    mem = [int(x) for x in mem]
    
    for noun in range(100):
        for verb in range(100):
            mem[1] = noun
            mem[2] = verb
            computer = Intcode()
            computer.memory = mem.copy()
            error = computer.run()
            if not error:
                if computer.memory[0] == 19690720:
                    break
        else:
            continue
        break
    print(100*noun + verb)
