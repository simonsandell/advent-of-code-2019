import asyncio
# pylint: disable=R1710
class Intcode:
    def __init__(self):
        self.OPCODES = {
            1:self.add,
            2:self.multiply,
            3:self.save,
            4:self.output,
            5:self.jumpiftrue,
            6:self.jumpiffalse,
            7:self.lessthan,
            8:self.equals,
            99:self.halt
            }

        self.memory = []
        self.cursor = 0
        self.modes = 0

        self.get_input = input
        self.send_output = print

    def get_parameter(self, n):
        return self.get_value(self.get_mode(n), self.memory[self.cursor + n])

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

    async def jumpiftrue(self, invert=False):
        # two parameters, if first param is non-zero
        # then set cursor to second parameter
        # both parameter mode dependent
        param_1 = self.get_parameter(1)
        param_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        if (param_1 and not invert) or (not param_1 and invert):
            # set cursor
            self.cursor = param_2
        else:
            self.cursor += 3
        return False

    async def jumpiffalse(self):
        return self.jumpiftrue(invert=True)

    async def lessthan(self):
        # 3 parameters, first two are mode dependent
        # if first param is less than second, store 1 in third else store 0
        param_1 = self.get_parameter(1)
        param_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        boolean = int(param_1 < param_2)

        target_position = self.memory[self.cursor+3]
        self.memory[target_position] = boolean

        self.cursor += 4
        return False

    async def equals(self):
        param_1 = self.get_parameter(1)
        param_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        boolean = int(param_1 == param_2)

        target_position = self.memory[self.cursor+3]
        self.memory[target_position] = boolean

        self.cursor += 4
        return False

    async def save(self):
        inp = await self.get_input()
        target_position = self.memory[self.cursor+1]
        self.memory[target_position] = inp
        self.cursor += 2

        return False

    async def output(self):
        out = self.get_value(self.get_mode(1), self.memory[self.cursor + 1])
        self.send_output(out)
        self.cursor += 2

        return False

    async def add(self):
        # tree parameters, three modes
        term_1 = self.get_value(self.get_mode(1), self.memory[self.cursor + 1])
        term_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        Sum = term_1 + term_2

        target_position = self.memory[self.cursor+3]
        self.memory[target_position] = Sum
        self.cursor += 4

        return False


    async def multiply(self):
        factor_1 = self.get_value(self.get_mode(1), self.memory[self.cursor + 1])
        factor_2 = self.get_value(self.get_mode(2), self.memory[self.cursor + 2])
        product = factor_1 * factor_2

        target_position = self.memory[self.cursor+3]
        self.memory[target_position] = product
        self.cursor += 4

        return False

    async def halt(self):
        self.cursor += 1

        return True

    async def run(self):
        while True:
            opcode = self.memory[self.cursor] % 100
            self.modes = self.memory[self.cursor] // 100

            if not opcode in self.OPCODES:
                raise ValueError("invalid opcode")
            halt = await self.OPCODES[opcode]()

            if halt:
                return False

        return True

with open("input", "r") as f:
    mem = f.read().split(",")
INITIAL_MEMORY = [int(x) for x in mem]


class Amplifier:
    def __init__(self, phase, name):
        self.name = name
        self.phase = phase
        self.phase_used = False

        self.next_amplifier = None
        self.previous_amplifier = None

        self.output = asyncio.Queue()

    async def handle_input(self):
        if not self.phase_used:
            self.phase_used = True
            return self.phase
        res = await self.previous_amplifier.get_output()
        return res

    async def get_output(self):
        return await self.output.get()


    def set_output(self, x):
        self.output.put_nowait(x)


    async def run_Intcode(self):
        computer = Intcode()
        computer.memory = INITIAL_MEMORY.copy()
        computer.get_input = self.handle_input
        computer.send_output = self.set_output
        await computer.run()

        return
