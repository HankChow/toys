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
        self.is_given = False

    def give(self, value):
        self.value = value
        self.nominees = []
        self.is_given = True

    def confirm(self, value):
        self.value = value
        self.nominees = []

    def clear(self):
        if len(self.nominees) == 1 and self.value == 0:
            self.value = self.nominees[0]
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
            numbers = list(map(lambda y: int(y), list(filter(lambda x: x in [str(n) for n in range(0, 10)], list(f.read())))))
        if len(numbers) != 81:
            print('Invalid sudoku')
            exit()
        for index, num in enumerate(numbers):
            if num > 0:
                column = index % 9
                row = (index - column) / 9
                self.cells[(row, column)].give(num)

    def display_sudoku(self):
        for i in range(9):
            row = self.get_cells_by_row(i)
            for j in range(9):
                print(('' if row[j].block % 2 == 0 else (Fore.BLACK + Back.WHITE)) + 
                    ('' if row[j].is_given else Fore.GREEN) + 
                    str(row[j].value if row[j].value != 0 else ' '), end=' ')
                print(Style.RESET_ALL, end='')
            print()

    def get_cells_by_row(self, row):
        cells = []
        for i in range(9):
            cells.append(self.cells[(row, i)])
        return cells

    def get_cells_by_column(self, column):
        cells = []
        for i in range(9):
            cells.append(self.cells[(i, column)])
        return cells

    def get_cells_by_block(self, block):
        cells = []
        for i in range(9):
            for j in range(9):
                if self.cells[(i, j)].block == block:
                    cells.append(self.cells[(i, j)])
        return cells

    def get_unsolved_count(self):
        count = 0
        for row in range(9):
            for column in range(9):
                if self.cells[(row, column)].value == 0:
                    count += 1
        return count

    # 遍历每一个 cell 并去除候选数，然后遍历 cell.clear() 一次
    def kill_nominees(self):
        previous_unsolved = None
        unsolved = self.get_unsolved_count()
        while(previous_unsolved != unsolved):
            for row in range(9):
                for column in range(9):
                    if self.cells[(row, column)].value == 0:
                        nominee_set = set(self.cells[(row, column)].nominees)
                        others_in_row = set(list(map(lambda x: x.value, self.get_cells_by_row(row))))
                        others_in_column = set(list(map(lambda x: x.value, self.get_cells_by_column(column))))
                        others_in_block = set(list(map(lambda x: x.value, self.get_cells_by_block(self.cells[(row, column)].block))))
                        self.cells[(row, column)].nominees = list(nominee_set - others_in_row - others_in_column - others_in_block)
            for row in range(9):
                for column in range(9):
                    self.cells[(row, column)].clear()
            previous_unsolved = unsolved
            unsolved = self.get_unsolved_count()
            
if __name__ == '__main__':
    s = Sudoku()
    s.read_sudoku('aaa')
    s.display_sudoku()
    s.kill_nominees()
    print()
    s.display_sudoku()
