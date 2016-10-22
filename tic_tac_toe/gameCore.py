#!/bin/env python3

print ('Start')

class gameCore(object):

    def __init__(self):
        self.field = {
                1: False
                , 2: False
                , 3: False
                , 4: False
                , 5: False
                , 6: False
                , 7: False
                , 8: False
                , 9: False 
                }

    def showField(self):
        self.showField = self.field
        for key, values in sorted(self.showField.items()):
            if values:
                self.showField[key] = 'X'
            else:
                self.showField[key] = 'O'

        self.row1 = [self.showField[1,2]]

        print (self.row1)
