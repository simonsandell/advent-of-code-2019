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


    def multiply(self):
        subject_1 = self.memory[self.cursor+1]
        subject_2 = self.memory[self.cursor+2]
        target = self.memory[self.cursor+3]
        self.memory[target] = self.memory[subject_1] * self.memory[subject_2]
        self.cursor += 4

    def halt(self):
        self.cursor += 1
        return True

    def run(self):
        while self.memory[self.cursor] in self.OPCODES:
            halt = self.OPCODES[self.memory[self.cursor]]()
            if halt:
                return
        print("ERROR: Unknown instruction")
        print(self.cursor)
        print(self.memory)
        sys.exit(1)

if __name__=="__main__":
    mem = []
    with open("./input", "r") as f:
        mem = f.read().split(",")
    mem = [int(x) for x in mem]
    
    noun = 12
    verb = 2

    mem[1] = noun
    mem[2] = verb
    computer = Intcode()
    computer.memory = mem
    computer.run()
    print(computer.memory[0])
