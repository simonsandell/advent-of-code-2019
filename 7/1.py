import itertools
import Intcode


permutations = list(itertools.permutations([0, 1, 2, 3, 4]))
output_values = []
for perm in permutations:
    input_value = 0
    for phase in perm:
        amplifier = Intcode.Amplifier(phase, input_value)
        output_value = amplifier.run_Intcode()
        input_value = output_value
    output_values.append(output_value)
print(sorted(output_values)[0])
