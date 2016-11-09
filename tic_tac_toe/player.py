#!/bin/env python3
'''
Random player for tic tac toe
'''

import numpy as np

class Player(object):
    '''parent class for player'''

    def __init__(self, player, game):
        self.player = player
        self.game = game

    def make_move(self, game, position):
        '''make a move TODO: should be inherited'''
        game.set_move(position, self.player)

    def get_field(self, game):
        '''ask the game_core for the field'''
        self.field = game.field[:]

    def calc_possible_moves(self):
        '''determine free tiles'''
        self.get_field(self.game)
        self.possible_moves = [
            idx for idx, value in enumerate(self.field) if value == 0
            ]

class AI_Player(Player):
    '''machine learning algorithm for tic tac toe'''

    def __init__(self, player, game):
        Player.__init__(self,player,game)
        self.field = []
        self.possible_moves = []




class RandomPlayer(Player):
    '''This player makes random moves'''

    def __init__(self, player, game):
        Player.__init__(self,player,game)
        self.field = []
        self.possible_moves = []

    def make_random_move(self):
        '''set a random move on a valid field'''
        self.calc_possible_moves()
        random_move = np.random.choice(self.possible_moves)
        self.make_move(self.game, random_move)
