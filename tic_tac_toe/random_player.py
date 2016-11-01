#!/bin/env python3
'''
Random player for tic tac toe
'''

import random


class RandomPlayer(object):

    def __init__(self, player, game):
        self.set_player(player)
        self.game = game

    def set_player(self, player):
        self.Player = player

    def make_move(self, game, position):
        game.setMove(position, self.Player)

    def getField(self, game):
        self.field = game.field[:]

    def calcPossibleMoves(self):
        self.getField(self.game)
        self.possibleMoves = [
            idx for idx, value in enumerate(self.field) if value == 0
            ]

    def makeRandomMove(self):
        self.calcPossibleMoves()
        randomMove = random.choice(self.possibleMoves)
        self.make_move(self.game, randomMove)
