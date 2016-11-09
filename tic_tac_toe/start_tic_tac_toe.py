#!/bin/env python3

'''
testing
'''
import game_core as gc
import player as p

Game1 = gc.GameCore()

RndPlayer1 = p.RandomPlayer(1, Game1)
RndPlayer2 = p.RandomPlayer(2, Game1)

while Game1.winner is None:
    RndPlayer1.make_random_move()
    if Game1.winner is None:
        RndPlayer2.make_random_move()

Game1.show_field()
print(Game1.winner)

'''
unit_test = ut.unit_test_ttt()
unit_test.run_game(unit_test)
'''
