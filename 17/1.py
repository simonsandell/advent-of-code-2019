import asyncio
import Intcode
import Tiles

if __name__ == '__main__':
    with open('input', 'r') as f:
        ASCII = [int(x) for x in f.read().strip().split(',')]
    comp = Intcode.Intcode()
    comp.memory = ASCII
    comp.increase_memory(10)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(comp.run())

    tiles = Tiles.Tiles()
    tiles.build_map(comp.output)

    tiles.find_intersections()
    print(tiles)
    print(tiles.get_sum_of_alignment_parameters())
