# pylint: disable=R1710,R0902
class Intcode:
    def __init__(self):
        self.OPCODES = {
            1:self.add,
            2:self.multiply,
            3:self.inputvalue,
            4:self.outputvalue,
            5:self.jumpiftrue,
            6:self.jumpiffalse,
            7:self.lessthan,
            8:self.equals,
            9:self.shiftrelativebase,
            99:self.halt
            }

        self.memory = []
        self.cursor = 0
        self.modes = 0
        self.relative_base = 0

        self.output = []

        self.input_method = input
        self.output_method = self.output.append

        self.killswitch = False

    def increase_memory(self, factor):
        self.memory.extend((len(self.memory)*(factor-1))*[0])

    def get_parameter(self, n, write=False):
        if write:
            mode = self.get_mode(n)
            if mode == 0:
                return self.memory[self.cursor + n]
            if mode == 2:
                return self.memory[self.cursor + n] + self.relative_base
            raise Exception('Invalid mode')
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

        # relative mode
        if mode == 2:
            return self.memory[param + self.relative_base]

    def get_mode(self, n):
        return self.modes % pow(10, n) // pow(10, n-1)

    async def shiftrelativebase(self):
        "opcode 9: shift-relative-base"
        param = self.get_parameter(1)
        self.relative_base += param
        self.cursor += 2

        return False

    async def jumpiftrue(self, invert=False):
        "opcode 5: jump-if-true"
        # two parameters, if first param is non-zero
        # then set cursor to second parameter
        # both parameter mode dependent
        param_1 = self.get_parameter(1)
        param_2 = self.get_parameter(2)
        if (param_1 and not invert) or (not param_1 and invert):
            # set cursor
            self.cursor = param_2
        else:
            self.cursor += 3
        return False

    async def jumpiffalse(self):
        "opcode 6: jump-if-false"
        return await self.jumpiftrue(invert=True)

    async def lessthan(self):
        "opcode 7: less-than"
        # 3 parameters, first two are mode dependent
        # if first param is less than second, store 1 in third else store 0
        param_1 = self.get_parameter(1)
        param_2 = self.get_parameter(2)
        boolean = int(param_1 < param_2)

        target_position = self.get_parameter(3, write=True)
        self.memory[target_position] = boolean

        self.cursor += 4
        return False

    async def equals(self):
        "opcode 8: equals"
        param_1 = self.get_parameter(1)
        param_2 = self.get_parameter(2)
        boolean = int(param_1 == param_2)

        target_position = self.get_parameter(3, write=True)
        self.memory[target_position] = boolean

        self.cursor += 4
        return False

    async def inputvalue(self):
        "opcode 3: input"
        inp = int(await self.input_method())
        target_position = self.get_parameter(1, write=True)
        self.memory[target_position] = inp
        self.cursor += 2

        return False

    async def outputvalue(self):
        "opcode 4: output"
        out = self.get_parameter(1)
        self.output_method(out)
        self.cursor += 2

        return False

    async def add(self):
        "opcode 1: add"
        term_1 = self.get_parameter(1)
        term_2 = self.get_parameter(2)
        Sum = term_1 + term_2

        target_position = self.get_parameter(3, write=True)
        self.memory[target_position] = Sum
        self.cursor += 4

        return False


    async def multiply(self):
        "opcode 2: multiply"
        factor_1 = self.get_parameter(1)
        factor_2 = self.get_parameter(2)
        product = int(factor_1 * factor_2)

        target_position = self.get_parameter(3, write=True)
        self.memory[target_position] = product
        self.cursor += 4

        return False

    async def halt(self):
        "opcode 99: halt"
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
            if self.killswitch:
                break

        return True
