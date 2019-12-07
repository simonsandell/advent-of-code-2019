import asyncio
import itertools
import Intcode2 as Intcode


def run_loop(perm):
    # setup initial conditions
    ampA = Intcode.Amplifier(perm[0], 'A')
    ampB = Intcode.Amplifier(perm[1], 'B')
    ampC = Intcode.Amplifier(perm[2], 'C')
    ampD = Intcode.Amplifier(perm[3], 'D')
    ampE = Intcode.Amplifier(perm[4], 'E')


    ampA.previous_amplifier = ampE
    ampB.previous_amplifier = ampA
    ampC.previous_amplifier = ampB
    ampD.previous_amplifier = ampC
    ampE.previous_amplifier = ampD

    ampA.next_amplifier = ampB
    ampB.next_amplifier = ampC
    ampC.next_amplifier = ampD
    ampD.next_amplifier = ampE
    ampE.next_amplifier = ampA

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            ampE.output.put(0),
            ampA.run_Intcode(),
            ampB.run_Intcode(),
            ampC.run_Intcode(),
            ampD.run_Intcode(),
            ampE.run_Intcode()
        )
    )
    res = loop.run_until_complete(ampE.output.get())
    return res

permutations = list(itertools.permutations([5, 6, 7, 8, 9]))
output_values = []
tasks = []

for perm in permutations:
    thruster_power = run_loop(perm)
    output_values.append(thruster_power)
print(sorted(output_values)[-1])
