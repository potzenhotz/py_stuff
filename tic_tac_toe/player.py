#!/bin/env python3
'''
Random player for tic tac toe
'''

import numpy as np

class Player(object):
    '''parent class for player'''

    def __init__(self, player, game_field):
        self.player = player
        self.game_field = game_field
        self.field = []
        self.possible_moves = []

    def make_move(self, position):
        '''make a move TODO: should be inherited'''
        self.game_field.set_move(position, self.player)

    def get_field(self):
        '''ask the game_core for the field'''
        self.field = self.game_field.field[:]

    def calc_possible_moves(self):
        '''determine free tiles'''
        self.get_field()
        self.possible_moves = [
            idx for idx, value in enumerate(self.field) if value == 0
            ]

class AIPlayer(Player):
    '''machine learning algorithm for tic tac toe'''

    def __init__(self, player, game_field):
        Player.__init__(self, player, game_field)
        self.field = []
        self.possible_moves = []




class RandomPlayer(Player):
    '''This player makes random moves'''

    def __init__(self, player, game_field):
        Player.__init__(self, player, game_field)
        self.field = []
        self.possible_moves = []

    def make_random_move(self):
        '''set a random move on a valid field'''
        self.calc_possible_moves()
        random_move = np.random.choice(self.possible_moves)
        self.make_move(random_move)
