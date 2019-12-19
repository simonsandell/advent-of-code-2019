import asyncio
import Intcode
import Tiles

def asciify(l):
    asciil = []
    for i, p in enumerate(l):
        p = str(p)
        for c in p:
            asciil.append(ord(c))
        if i + 1 != len(l):
            asciil.append(ord(','))
        else:
            asciil.append(ord('\n'))
    return asciil

def best_possible(progs, skip_progs):
    p = progs.copy()
    while True:
        b = get_max_value(p)
        if b in skip_progs:
            del p[b]
        else:
            return b

def greedy_algorithm(moves, skip_progs=[]):
    programs = []
    failed = False
    moves_copy = moves.copy()
    while len(programs) < 3:
        progs = get_possible_programs(moves_copy)
        best_prog = best_possible(progs, skip_progs)
        moves_copy = remove_substring(list(best_prog), moves_copy)
        programs.append(best_prog)
    if moves_copy != ['X']*len(moves):
        failed = True
    return programs, failed

def get_possible_programs(moves):
    i = 2
    max_value = 0
    progs = {}
    while i < 12:
        ss, value = get_substrings(i, moves)
        if value > max_value:
            max_value = value
        if value < max_value:
            break
        i += 2
        progs.update(ss)
    return progs

def get_substrings(n, string):
    ss = {}
    for i in range(len(string) - n + 1):
        tup = tuple(string[i:i+n])
        if tup not in ss:
            ss[tup] = n*get_nonoverlapping_occurence(list(tup), string)
        if 'X' in tup:
            ss[tup] = 0
        i += 1
    maxcount = 0
    best = None
    for tup in ss:
        if ss[tup] > maxcount:
            maxcount = ss[tup]
            best = tup
    return ss, maxcount*n

def get_unique_lengths(string):
    unique = []
    for item in string:
        if isinstance(item, int):
            if item not in unique:
                unique.append(item)
    return unique

def get_nonoverlapping_occurence(substring, string):
    l = len(substring)
    i = 0
    c = 0
    while i < len(string):
        if string[i:(i+l)] == substring:
            c += 1
            i += l
        else:
            i += 1
    return c

def remove_substring(substring, string, subst = 'X'):
    l = len(substring)
    i = 0
    c = 0
    rem = string.copy()
    while i < len(string):
        if string[i:(i+l)] == substring:
            rem[(i):(i + l)] = [subst]*l
            c += 1
            i += l
        else:
            i += 1
    return rem

def get_max_value(programs):
    max_val = 0
    best_prog = None
    for k in programs:
        if programs[k] > max_val:
            max_val = programs[k]
            best_prog = k
    return best_prog

if __name__ == '__main__':
    with open('input', 'r') as f:
        ASCII = [int(x) for x in f.read().strip().split(',')]
    comp = Intcode.Intcode()
    comp.memory = ASCII.copy()
    comp.increase_memory(10)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(comp.run())

    save_output = comp.output.copy()

    tiles = Tiles.Tiles()
    tiles.build_map(comp.output)
    tiles.find_intersections()

    moves = tiles.get_robot_move_instruction()

    skip_programs = []
    failed = True
    while failed:
        programs, failed = greedy_algorithm(moves, skip_programs)
        skip_programs.append(programs[0])

    moves_copy = moves.copy()
    for p,n in zip(programs, ['A', 'B', 'C']):
        moves_copy = remove_substring(list(p), moves_copy, n)
    i = 0
    proglength = {
        'A':len(programs[0]),
        'B':len(programs[1]),
        'C':len(programs[2])
        }
    progdict = {
        'A':list(programs[0]),
        'B':list(programs[1]),
        'C':list(programs[2])
        }
    program_sequence = []
    while i < len(moves_copy):
        program_sequence.append(moves_copy[i])
        i += proglength[moves_copy[i]]
    reconstructed = []
    for p in program_sequence:
        reconstructed.extend(progdict[p])
    if reconstructed != moves:
        raise Exception("Reconstruction failed")

    #prepare input
    main_movement_routine = asciify(program_sequence)
    A_movement_function = asciify(progdict['A'])
    B_movement_function = asciify(progdict['B'])
    C_movement_function = asciify(progdict['C'])
    video = [ord('n'), ord('\n')]

    comp_input = []
    comp_input.extend(main_movement_routine)
    comp_input.extend(A_movement_function)
    comp_input.extend(B_movement_function)
    comp_input.extend(C_movement_function)
    comp_input.extend(video)
    comp_input.reverse()

    async def comp_input_method():
        return comp_input.pop()

    # reset computer
    modified_ASCII = ASCII.copy()
    modified_ASCII[0] = 2
    comp = Intcode.Intcode()
    comp.memory = modified_ASCII
    comp.increase_memory(100)

    comp.input_method = comp_input_method

    loop = asyncio.get_event_loop()
    loop.run_until_complete(comp.run())
    print(comp.output[-1])
