#!/bin/env python3
#testing
import gameCore as gc
import randomPlayer as rp

game1 = gc.gameCore()

rndPlayer = rp.randomPlayer(1, game1)


#if game1.isValidMove(2):
#    pass

#print(game1.hashField)
#print(game1.winningCombination[1][1])

#game1.evalField()

#print('move1')
game1.setMove(0,1)
#print('move2')
game1.setMove(1,1)
#print('move3')
#game1.setMove(2,1)

#game1.createHashWinningValues()
#game1.showField()


#print(game1.whoGoesFirst())
rndPlayer.calcPossibleMoves()
print(rndPlayer.possibleMoves)

rndPlayer.makeRandomMove()
game1.showField()
