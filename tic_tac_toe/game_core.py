#!/bin/env python3
########################################################################
# Job of the game field:
# -Set field
# -show_field
# -setMove
# -isValidMove
# -evalField
# -setWhoGoesFirst
# -changeField
# -raiseFieldisOccupied
# -
########################################################################

import random
import numpy as np
import pandas as pd


class GameCore(object):
    """This is the Master Chief of the field"""

    def __init__(self):
        self.field = []
        #self.winning_hash_values = []
        #self.winning_hash_values_p1 = []
        #self.winning_hash_values_p2 = []
        self.winner = None

        self.reset_field()
        self.create_winning_combination()
        #self.create_hash_winning_values()

    def reset_field(self):
        """resets the field"""
        self.field = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
            ]

    def create_winning_combination(self):
        """set valid winning combinations"""
        self.winning_combination = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

    def show_field(self):
        """displays the field to the prompt"""
        buffer_show_field = self.field[:]
        for idx, value in enumerate(buffer_show_field):
            if value == 0:
                buffer_show_field[idx] = '#'
            elif value == 1:
                buffer_show_field[idx] = 'X'
            elif value == 2:
                buffer_show_field[idx] = 'O'

        print('Current Field:')
        print(
            buffer_show_field[0], buffer_show_field[1], buffer_show_field[2]
            )
        print(
            buffer_show_field[3], buffer_show_field[4], buffer_show_field[5]
            )
        print(
            buffer_show_field[6], buffer_show_field[7], buffer_show_field[8]
            )

    def is_valid_move(self, position):
        """check if move is in range of field"""
        if self.eval_field():
            return False
        elif position in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            if self.field[position] == 0:
                return True
        return False

    def set_move(self, position, player):
        '''change state of tile in field'''
        if self.is_valid_move(position):
            self.change_tile_status(position, player)
            self.eval_field()
            if (self.winner == 1 or self.winner == 2):
                print('Player %s wins.' % self.winner)
            elif (self.winner == 0):
                print('Draw!')

        else:
            self.raise_field_is_duplicated(position)

    def change_tile_status(self, position, player):
        '''change status of tile in field'''
        self.field[position] = player

    def eval_field(self):
        '''check if a player has won'''
        for i in range(1, 3):
            for row_x in self.winning_combination:
                if (self.field[row_x[0]] == i and
                        self.field[row_x[1]] == i and
                        self.field[row_x[2]] == i):
                    self.winner = i
                    return True
        if 0 not in self.field:
            self.winner = 0
        return False

    def raise_field_is_duplicated(self, position):
        '''TODO: write propper error code'''
        print('Move is not valid ', position)

    def who_goes_first(self):
        '''random decision who goes first'''
        first_player = random.randint(1, 2)
        return first_player

    def create_hash_value(field):
        '''use python internal hash algorithm'''
        hash_value = hash(tuple(field))
        return hash_value
    """
    def create_hash_table(self):
        '''create the table for hash translation'''

    def inser_into_hash_table():
    """    
