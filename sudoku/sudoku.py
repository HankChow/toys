#!/usr/bin/env python3
# coding: utf-8

from colorama import *
from functools import reduce

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
        return self.value


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
                    ('' if row[j].is_given else Fore.BLUE + Style.BRIGHT) + 
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

    # 当一个 cell 确定后，必须调用此方法，去除与该 cell 同一 row/column/block 的其它 cell 的候选数
    def suppress(self, cell, value):
        for row in range(9):
            for column in range(9):
                if row == cell.row or column == cell.column or self.cells[(row, column)].block == cell.block:
                    if value in self.cells[(row, column)].nominees:
                        self.cells[(row, column)].nominees.remove(value)

    # 遍历每一个 cell 并去除候选数，然后遍历 cell.clear() 一次
    def kill_nominees(self):
        previous_unsolved = None
        unsolved = self.get_unsolved_count()
        while(previous_unsolved != unsolved):
            for row in range(9):
                for column in range(9):
                    # 当某个 cell 为空时
                    if self.cells[(row, column)].value == 0:
                        nominee_set = set(self.cells[(row, column)].nominees)
                        others_in_row = set(list(map(lambda x: x.value, self.get_cells_by_row(row))))
                        others_in_column = set(list(map(lambda x: x.value, self.get_cells_by_column(column))))
                        others_in_block = set(list(map(lambda x: x.value, self.get_cells_by_block(self.cells[(row, column)].block))))
                        self.cells[(row, column)].nominees = list(nominee_set - others_in_row - others_in_column - others_in_block)
            for row in range(9):
                for column in range(9):
                    newly_fill = self.cells[(row, column)].clear()
                    self.suppress(self.cells[(row, column)], newly_fill)
            previous_unsolved = unsolved
            unsolved = self.get_unsolved_count()

    # 遍历每一个 row/column/block ，如果 row/column/block 内唯一有一个未填的 cell 拥有某个候选数，这个未填的 cell 就可以 confirm 这个候选数
    def unique_nominee(self):
        previous_unsolved = None
        unsolved = self.get_unsolved_count()
        while(previous_unsolved != unsolved):
            # row
            for row in range(9):
                empty_cells = list(filter(lambda x: x.value == 0, self.get_cells_by_row(row)))
                if len(empty_cells) > 1:
                    for index, value in enumerate(empty_cells):
                        others_nominees = set(reduce(lambda x, y: x + y, list(map(lambda w: w.nominees, list(filter(lambda z: empty_cells.index(z) != index, empty_cells))))))
                        this_nominees = list(set(value.nominees) - others_nominees)
                        if len(this_nominees) == 1:
                            unique_cell = empty_cells[index]
                            self.cells[(unique_cell.row, unique_cell.column)].confirm(this_nominees[0])
                            self.suppress(self.cells[(unique_cell.row, unique_cell.column)], this_nominees[0])
            # column
            for column in range(9):
                empty_cells = list(filter(lambda x: x.value == 0, self.get_cells_by_column(column)))
                if len(empty_cells) > 1:
                    for index, value in enumerate(empty_cells):
                        others_nominees = set(reduce(lambda x, y: x + y, list(map(lambda w: w.nominees, list(filter(lambda z: empty_cells.index(z) != index, empty_cells))))))
                        this_nominees = list(set(value.nominees) - others_nominees)
                        if len(this_nominees) == 1:
                            unique_cell = empty_cells[index]
                            self.cells[(unique_cell.row, unique_cell.column)].confirm(this_nominees[0])
                            self.suppress(self.cells[(unique_cell.row, unique_cell.column)], this_nominees[0])
            # block
            for block in range(9):
                empty_cells = list(filter(lambda x: x.value == 0, self.get_cells_by_block(block)))
                if len(empty_cells) > 1:
                    for index, value in enumerate(empty_cells):
                        others_nominees = set(reduce(lambda x, y: x + y, list(map(lambda w: w.nominees, list(filter(lambda z: empty_cells.index(z) != index, empty_cells))))))
                        this_nominees = list(set(value.nominees) - others_nominees)
                        if len(this_nominees) == 1:
                            unique_cell = empty_cells[index]
                            self.cells[(unique_cell.row, unique_cell.column)].confirm(this_nominees[0])
                            self.suppress(self.cells[(unique_cell.row, unique_cell.column)], this_nominees[0])
            previous_unsolved = unsolved
            unsolved = self.get_unsolved_count()


    # 按照优先级，往复遍历一次所有求值方法
    def whole_solve(self):
        priority = [self.kill_nominees, self.unique_nominee]
        whole = priority[:-1] + priority[::-1]
        previous_unsolved = None
        unsolved = self.get_unsolved_count()
        while(previous_unsolved != unsolved):
            for method in whole:
                method()
            previous_unsolved = unsolved
            unsolved = self.get_unsolved_count()

            
if __name__ == '__main__':
    s = Sudoku()
    s.read_sudoku('aaa')
    s.display_sudoku()
    s.whole_solve()
    print()
    s.display_sudoku()
