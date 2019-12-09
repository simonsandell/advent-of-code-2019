import Intcode


memory_factor = 100

# Test 1
TEST_CODE = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")
TEST_CODE = [int(x) for x in TEST_CODE]
computer = Intcode.Intcode()
computer.memory = TEST_CODE.copy()
computer.increase_memory(memory_factor)
computer.run()
print('Test 1', computer.output == TEST_CODE)

#Test 2
TEST_CODE = "1102,34915192,34915192,7,4,7,99,0".split(",")
TEST_CODE = [int(x) for x in TEST_CODE]
computer = Intcode.Intcode()
computer.memory = TEST_CODE.copy()
computer.increase_memory(memory_factor)
computer.run()
print('Test 2', len(str(computer.output[0])) == 16)

#Test 3
TEST_CODE = "104,1125899906842624,99".split(",")
TEST_CODE = [int(x) for x in TEST_CODE]
computer = Intcode.Intcode()
computer.memory = TEST_CODE.copy()
computer.increase_memory(memory_factor)
computer.run()
print('Test 3', computer.output[0] == TEST_CODE[1])

# Real run

with open("input", "r") as f:
    mem = f.read().split(",")
INITIAL_MEMORY = [int(x) for x in mem]
computer = Intcode.Intcode()
computer.memory = INITIAL_MEMORY.copy()
computer.increase_memory(memory_factor)
computer.run()
print(computer.output[0])
print(computer.output)
