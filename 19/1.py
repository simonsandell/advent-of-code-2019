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

    spacemap = Tiles.Tiles()
    positions = []
    for x in range(50):
        for y in range(50):
            compout = str(query_comp((x, y)))
            spacemap.panels[(x, y)] = compout
    print(spacemap)
