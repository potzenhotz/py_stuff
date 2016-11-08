#!/bin/env python3
'''
testing
'''
import game_core as gc
import random_player as rp
#import unit_test_ttt as ut

#'''
game1 = gc.GameCore()

rnd_player1 = rp.RandomPlayer(1, game1)
rnd_player2 = rp.RandomPlayer(2, game1)

#if game1.isValidMove(2):
#    pass

#print(game1.hashField)
#print(game1.winningCombination[1][1])

#game1.evalField()
#print(game1.field)
#print('move1')
#game1.set_move(0,1)
#print('move2')
#game1.set_move(1,1)
#print('move3')
#game1.set_move(2,1)
#game1.set_move(3,1)

#]game1.createHashWinningValues()
#game1.show_field()


#print(game1.whoGoesFirst())
#rndPlayer.calcPossibleMoves()
#print(rndPlayer.possibleMoves)
#'''
while (game1.winner is None):
    rnd_player1.make_random_move()
    if (game1.winner is None):
        rnd_player2.make_random_move()

game1.show_field()
print(game1.winner)

#'''

'''
unit_test = ut.unit_test_ttt()
unit_test.run_game(unit_test)
'''




