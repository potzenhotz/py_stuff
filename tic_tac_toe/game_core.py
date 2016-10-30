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


class GameCore(object):
    """This is the Master Chief of the field"""

    def __init__(self):
        self.field = []
        self.winning_hash_values = []
        self.winning_hash_values_p1 = []
        self.winning_hash_values_p2 = []
        self.winner = None

        self.reset_field()
        self.create_winning_combination()
        self.create_hash_winning_values()

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

    @staticmethod
    def create_hash_value(field):
        '''use python internal hash algorithm'''
        hash_value = hash(tuple(field))
        return hash_value

    def create_hash_winning_values(self):
        """translate winning values into hash value"""
        for player_counter in range(1, 3):
            for row_x in range(len(self.winning_combination)):
                self.change_tile_status(
                    self.winning_combination[row_x][0], player_counter
                    )
                self.change_tile_status(
                    self.winning_combination[row_x][1], player_counter
                    )
                self.change_tile_status(
                    self.winning_combination[row_x][2], player_counter
                    )

                buffer_hash_value = self.create_hash_value(self.field)
                self.winning_hash_values.append(buffer_hash_value)
                if player_counter == 1:
                    self.winning_hash_values_p1.append(buffer_hash_value)
                elif player_counter == 2:
                    self.winning_hash_values_p2.append(buffer_hash_value)

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
        if position in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            if self.field[position] == 0:
                return True
        return False

    def set_move(self, position, player):
        '''change state of tile in field'''
        if self.is_valid_move(position):
            self.change_tile_status(position, player)
            if self.eval_field():
                print('Player %s wins.' % self.winner)
        else:
            self.raise_field_is_duplicated(position)

    def change_tile_status(self, position, player):
        '''change status of tile in field'''
        self.field[position] = player

    def eval_field(self):
        '''evaluate field for a winner'''
        current_hash_field = self.create_hash_value(self.field)
        if current_hash_field in self.winning_hash_values_p1:
            self.winner = 1
            return True
        elif current_hash_field in self.winning_hash_values_p2:
            self.winner = 2
            return True

    def raise_field_is_duplicated(self, position):
        '''TODO: write propper error code'''
        print('Move is not valid ', position)

    def who_goes_first(self):
        '''random decision who goes first'''
        first_player = random.randint(1, 2)
        return first_player
