#!/bin/env python3
########################################################################
# Job of the game field:
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

class gameCore(object):

    def __init__(self):
        player1 = 1
        player2 = 2
        self.resetField() 

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

    def resetField(self):
        self.field = [
                0, 0, 0,
                0, 0, 0,
                0, 0, 0 
                ]

    def createHashValue(self, field):
        hashValue = hash(tuple(field)) 
        return hashValue


    def createHashWinningValues(self):
        self.winningHashValues = []
        for playerCounter in range(1,3):
            for rowX in range(len(self.winningCombination)):
                self.setRawMove(self.winningCombination[rowX][0], playerCounter)
                self.setRawMove(self.winningCombination[rowX][1], playerCounter)
                self.setRawMove(self.winningCombination[rowX][2], playerCounter)

                self.winningHashValues = self.createHashValue(self.field)
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
        if position in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if self.field[position] == 0:
                return True
            else:
                return False
        else:
            return False
    
    def setRawMove(self, position, player):
        self.changeFieldStatus(position, player)
        
    def setMove(self, position, player):
        if self.isValidMove(position):
            self.changeFieldStatus(position, player)
            self.evalField()
        else:
            self.raiseFieldIsDuplicated(position)

    def changeFieldStatus(self, position, player):
        self.field[position] = player

    def evalField(self):
        for i in range(len(self.winningCombination)):
            counter_3_p1 = 0
            counter_3_p2 = 0
            for j in range(3):
                if self.field[self.winningCombination[i][j]] == 1:
                    counter_3_p1 +=1
                    if counter_3_p1 ==3:
                        print("Player 1 wins.")
                elif self.field[self.winningCombination[i][j]] == 2:
                    counter_3_p2 +=1
                    if counter_3_p2 ==3:
                        print("Player 2 wins.")

    def raiseFieldIsDuplicated(self, position):
        print('raise Error')




