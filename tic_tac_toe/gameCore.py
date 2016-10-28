#!/bin/env python3
########################################################################
#a Job of the game field:
# -Set field
# -showField
# -setMove
# -isValidMove
# -evalField
# -setWhoGoesFirst
# -changeField
# -raiseFieldisOccupied
# -
########################################################################

import random 

class gameCore(object):

    def __init__(self):
        player1 = 1
        player2 = 2
        self.resetField() 
        self.createWinningCombination()
        self.createHashWinningValues()

    def resetField(self):
        self.field = [
                0, 0, 0,
                0, 0, 0,
                0, 0, 0 
                ]


    def createWinningCombination(self):
        self.winningCombination = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [2,4,6]
        ]


    def createHashValue(self, field):
        hashValue = hash(tuple(field)) 
        return hashValue


    def createHashWinningValues(self):
        self.winningHashValues = []
        self.winningHashValuesP1 = []
        self.winningHashValuesP2 = []
        for playerCounter in range(1,3):
            for rowX in range(len(self.winningCombination)):
                self.changeFieldStatus(self.winningCombination[rowX][0], playerCounter)
                self.changeFieldStatus(self.winningCombination[rowX][1], playerCounter)
                self.changeFieldStatus(self.winningCombination[rowX][2], playerCounter)

                bufferHashValue = self.createHashValue(self.field)
                self.winningHashValues.append(bufferHashValue)
                if playerCounter == 1:
                    self.winningHashValuesP1.append(bufferHashValue)
                elif playerCounter == 2:
                    self.winningHashValuesP2.append(bufferHashValue)

                self.resetField()


    def showField(self):
        self.showField = self.field[:]
        for idx, value in enumerate(self.showField):
            if value == 0:
                self.showField[idx] = '#'
            elif value == 1:
                self.showField[idx] = 'X'
            elif value == 2:
                self.showField[idx] = 'O'

        print ('Current Field:')
        print (self.showField[0],self.showField[1], self.showField[2])
        print (self.showField[3],self.showField[4], self.showField[5])
        print (self.showField[6],self.showField[7], self.showField[8])
        

    def isValidMove(self, position):
        if position in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            if self.field[position] == 0:
                return True
            else:
                return False
        else:
            return False
        

    def setMove(self, position, player):
        if self.isValidMove(position):
            self.changeFieldStatus(position, player)
            if self.evalField():
                print('Player %s wins.' % self.winner)
        else:
            self.raiseFieldIsDuplicated(position)


    def changeFieldStatus(self, position, player):
        self.field[position] = player


    def evalField(self):
        currentHashField = self.createHashValue(self.field)
        if currentHashField in self.winningHashValuesP1:
            self.winner = 1
            return True
        elif currentHashField in self.winningHashValuesP2:
            self.winner = 2
            return True


    def raiseFieldIsDuplicated(self, position):
        print('Move is not valid ', position)

    def whoGoesFirst(self):
        self.firstPlayer = random.randint(1,2)
        return self.firstPlayer



