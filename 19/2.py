import asyncio
import Intcode
import Tiles



if __name__ == '__main__':
    with open('input', 'r') as f:
        PROG = [int(x) for x in f.read().strip().split(',')]

    comp = Intcode.Intcode()
    comp.input_queue = asyncio.Queue()
    comp.input_method = comp.input_queue.get
    comp.output_queue = asyncio.Queue()
    comp.output_method = comp.output_queue.put_nowait
    def query_comp(pos):
        comp.memory = PROG.copy()
        comp.increase_memory(10)
        comp.cursor = 0
        comp.relative_base = 0

        comp.input_queue.put_nowait(pos[0])
        comp.input_queue.put_nowait(pos[1])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comp.run())
        return comp.output_queue.get_nowait()


    def find_top_border(pos):
        c = query_comp(pos)
        while c != 1:
            pos = (pos[0], pos[1] + 1)
            c = query_comp(pos)
        return pos

    def spacecraft_fits(pos):
        otherpos = (pos[0] - 99, pos[1] + 99)
        if query_comp(otherpos) == 0:
            return False
        return True
    pos = (100, 0)
    borderpos = find_top_border(pos)
    while not spacecraft_fits(borderpos):
        pos = (borderpos[0] + 1, borderpos[1])
        borderpos = find_top_border(pos)
    t = (borderpos[0] - 99, borderpos[1])
    ans = (t[0])*10000 + t[1]
    print(ans)
