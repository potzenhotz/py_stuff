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
        self.field = {
                1: 0, 2: 0, 3: 0,
                4: 0, 5: 0, 6: 0,
                7: 0, 8: 0, 9: 0 
                }
        
        self.hashField = {
                1: 2**0, 2: 2**1, 3: 2**2,
                4: 2**3, 5: 2**4, 6: 2**5,
                7: 2**6, 8: 2**7, 9: 2**8,
                }

        self.winningCombination = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                [1,4,7],
                [2,5,8],
                [3,6,9],
                [1,5,9],
                [3,5,7]
                ]

        #here should be a reference to winningCombination
        #need to think of a good loop 
        self.winningHashValues = [
                self.hashField[1] + self.hashField[2] + self.hashField[3],
                self.hashField[4] + self.hashField[5] + self.hashField[6],
                self.hashField[7] + self.hashField[8] + self.hashField[9],
                self.hashField[1] + self.hashField[4] + self.hashField[7],
                self.hashField[2] + self.hashField[5] + self.hashField[8],
                self.hashField[3] + self.hashField[6] + self.hashField[9],
                self.hashField[1] + self.hashField[5] + self.hashField[9],
                self.hashField[3] + self.hashField[5] + self.hashField[7],
                ]


    def showField(self):
        self.showField = self.field.copy()
        for key, values in sorted(self.showField.items()):
            if values == 0:
                self.showField[key] = '#'
            elif values == 1:
                self.showField[key] = 'X'
            elif values == 2:
                self.showField[key] = 'O'

        print ('Current Field:')
        print (self.showField[1],self.showField[2], self.showField[3])
        print (self.showField[4],self.showField[5], self.showField[6])
        print (self.showField[7],self.showField[8], self.showField[9])
        
    def isValidMove(self, position):
        if position in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if self.field[position] == 0:
                return True
            else:
                return False
        else:
            return False
        
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




