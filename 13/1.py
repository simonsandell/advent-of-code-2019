import Tiles
import Intcode

with open('input', 'r') as f:
    game = f.read().split(',')
game = [int(x) for x in game]

COMP = Intcode.Intcode()
COMP.memory = game
COMP.increase_memory(10)
COMP.run()

GAMEBOARD = Tiles.GameSurface()
for x,y,t in zip(COMP.output[0::3],COMP.output[1::3], COMP.output[2::3]):
    GAMEBOARD.set_color((x,y),t)

print(GAMEBOARD)
print(GAMEBOARD.tilecount[2])
