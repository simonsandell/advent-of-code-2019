import asyncio
import Tiles
import Intcode
import random

class Repairdroid:
    def __init__(self, program):
        self.x = 0
        self.y = 0
        self.surface = Tiles.Hallway()
        self.output = []
        self.Computer = Intcode.Intcode()
        self.Computer.memory = program
        self.Computer.increase_memory(10)

        self.Computer.output = asyncio.Queue()
        self.Computer.output_method = self.Computer.output.put_nowait

        self.output = asyncio.Queue()
        self.Computer.input_method = self.output.get

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self.Computer.run(), self.run_loop()))
        loop.close()

    async def run_loop(self):
        while True:
            win = await self.try_move()
            if win:
                break

    async def get_droid_status(self):
        status = await self.Computer.output.get()
        return status

    @staticmethod
    def dir_to_tuple(move):
        if move == 1:
            return (0, 1)
        if move == 2:
            return (0, -1)
        if move == 3:
            return (-1, 0)
        if move == 4:
            return (1, 0)

    @staticmethod
    def invert_dir(d):
        if d == 1:
            return 2
        if d == 1:
            return 1
        if d == 3:
            return 4
        if d == 4:
            return 3

    def update_surface(self, move, status):
        tup = Repairdroid.dir_to_tuple(move)
        selfpos = (self.x, self.y)
        pos = (self.x + tup[0], self.y + tup[1])

        if status == 0:
            self.surface.set_color(pos, 1)
            return False
        if status == 1:
            self.surface.set_color(pos, 0)
            self.surface.set_color(selfpos, 3)
            self.x = pos[0]
            self.y = pos[1]
            return False
        if status == 2:
            self.surface.set_color(pos, 4)
            self.surface.set_color(selfpos, 3)
            self.x = pos[0]
            self.y = pos[1]
            return True

    async def try_move(self):
        moves = []
        if self.surface.get_color((self.x, self.y+1)) == 2:
            moves.append(1)
        if self.surface.get_color((self.x, self.y-1)) == 2:
            moves.append(2)
        if self.surface.get_color((self.x-1, self.y)) == 2:
            moves.append(3)
        if self.surface.get_color((self.x+1, self.y)) == 2:
            moves.append(4)
        if len(moves) > 0:
            move = random.choice(moves)
        else:
            if self.surface.get_color((self.x, self.y+1)) == 3:
                moves.append(1)
            if self.surface.get_color((self.x, self.y-1)) == 3:
                moves.append(2)
            if self.surface.get_color((self.x-1, self.y)) == 3:
                moves.append(3)
            if self.surface.get_color((self.x+1, self.y)) == 3:
                moves.append(4)
            move = random.choice(moves)
        # we have a candidate move.
        self.output.put_nowait(move)
        status = await self.get_droid_status()
        win = self.update_surface(move, status)
        return win


if __name__ == "__main__":
    with open('input', 'r') as f:
        prog = f.read().strip().split(',')
    PROG = [int(x) for x in prog]

    robo = Repairdroid(PROG)
    robo.run()
