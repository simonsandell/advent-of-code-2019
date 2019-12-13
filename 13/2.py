import sys

import Tiles
import Intcode
import Joystick


with open('input', 'r') as f:
    game = f.read().split(',')
game = [int(x) for x in game]
game[0] = 2

COMP = Intcode.Intcode()
COMP.memory = game
COMP.increase_memory(10)
GAMEBOARD = Tiles.GameSurface()
if len(sys.argv) > 1:
    COMP.input_method = Joystick.touch_the_stick
else:
    COMP.input_method = GAMEBOARD.botplayer
COMP.output_method = GAMEBOARD.read_instructions

COMP.run()
