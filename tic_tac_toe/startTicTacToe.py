#!/bin/env python3

import gameCore as gc

game1 = gc.gameCore()


game1.showField()

if game1.isValidMove(2):
    pass

print(game1.hashField)
print(game1.winningCombination[1][1])


game1.evalField()


print('move1')
game1.setMove(1,1)
print('move2')
game1.setMove(2,1)
print('move3')
game1.setMove(3,1)
