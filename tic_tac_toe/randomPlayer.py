#!/bin/env python3
#Random player for tic tac toe

import random

class randomPlayer(object):

    def __init__(self, player, game):
        self.setPlayer(player)        
        self.game = game

    def setPlayer(self, player):
        self.Player = player

    def makeMove(self, game, position):
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
        self.makeMove(self.game, randomMove)
