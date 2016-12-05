#!/bin/env python3
'''
Unit Test
'''
import game_core as gc
import random_player as rp


class unit_test_ttt(object):
    '''unit test for tic tac toe'''

    def __init__(self):
        self.unit_test = False
        self.player1 = None
        self.player2 = None

    def set_field(self):
        '''sets the game field'''
        self.ut_field = gc.GameCore()

    def set_rnd_player(self, field):
        '''set a rnd player'''
        self.player1 = rp.RandomPlayer(1, field)
        self.player2 = rp.RandomPlayer(2, field)

    def play_game(self):
        self.player1.make_random_move()
        self.player2.make_random_move()
        self.player1.make_random_move()
        self.player2.make_random_move()
        self.player1.make_random_move()
        self.player2.make_random_move()
        self.player1.make_random_move()

    def run_game(self, ut_object):
        ut_object.set_field()
        ut_object.set_rnd_player(ut_object.ut_field)
        ut_object.play_game()
        print(ut_object.ut_field.show_field())
        print('Winner:', ut_object.ut_field.winner)

