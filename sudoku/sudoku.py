#!/usr/bin/env python3
# coding: utf-8

from colorama import *

class Cell(object):
    
    def __init__(self, row, column, value=0):
        self.row = row
        self.column = column
        self.block = ((row // 3) * 3) + (column // 3)
        self.value = value
        self.nominees = [n for n in range(1, 10)] if value == 0 else []

    def confirm(self, value):
        self.value = value
        self.nominees = []

class Sudoku(object):

    def __init__(self):
        self.cells = {}
        for row in range(9):
            for column in range(9):
                cell = Cell(row, column)
                self.cells[(row, column)] = cell

    def read_sudoku(self, filename):
        with open(filename) as f:
            numbers = list(map(lambda y: int(y), list(filter(lambda x: x in [n for n in range(0, 10)], list(f.read())))))
        if len(s) != 81:
            print('Invalid sudoku')
            exit()
        for index, num in enumerate(numbers):
            if num > 0:
                column = index % 9
                row = (index - column) / 9
                self.cells[(row, column)].confirm(num)

    def get_numbers_by_row(self, row):
        nums = []
        for i in range(9):
            nums.append(self.cells[(row, i)])
        return nums

    def get_numbers_by_column(self, column):
        nums = []
        for i in range(9):
            nums.append(self.cells[(i, column)])
        return nums

    def get_numbers_by_block(self, block):
        nums = []
        for i in range(9):
            for j in range(9):
                if self.cells[(i, j)].block == block:
                    nums.append(self.cells[(i, j)])
        return nums
            
if __name__ == '__main__':
    pass
