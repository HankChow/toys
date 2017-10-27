#!/usr/bin/env python3
# coding: utf-8

import itertools
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
        self.initiative_unsolved = 81

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
        self.initiative_unsolved = self.get_unsolved_count()

    def display_sudoku(self):
        for i in range(9):
            row = self.get_cells_by('row', i)
            for j in range(9):
                print(('' if row[j].block % 2 == 0 else (Fore.BLACK + Back.WHITE)) + 
                    ('' if row[j].is_given else Fore.BLUE + Style.BRIGHT) + 
                    str(row[j].value if row[j].value != 0 else ' '), end=' ')
                print(Style.RESET_ALL, end='')
            print()
        print('-' * 18)
        print('{solved}/{initiative} solved.'.format(solved=(self.initiative_unsolved - self.get_unsolved_count()), initiative=self.initiative_unsolved))

    def get_cells_by(self, unit, num):
        cells = []
        if unit == 'row':
            for i in range(9):
                cells.append(self.cells[(num, i)])
        elif unit == 'column':
            for i in range(9):
                cells.append(self.cells[(i, num)])
        elif unit == 'block':
            for i in range(9):
                for j in range(9):
                    if self.cells[(i, j)].block == num:
                        cells.append(self.cells[(i, j)])
        else:
            return None
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
                        others_in_row = set(list(map(lambda x: x.value, self.get_cells_by('row', row))))
                        others_in_column = set(list(map(lambda x: x.value, self.get_cells_by('column', column))))
                        others_in_block = set(list(map(lambda x: x.value, self.get_cells_by('block', self.cells[(row, column)].block))))
                        self.cells[(row, column)].nominees = list(nominee_set - others_in_row - others_in_column - others_in_block)
            for row in range(9):
                for column in range(9):
                    newly_fill = self.cells[(row, column)].clear()
                    self.suppress(self.cells[(row, column)], newly_fill)
            previous_unsolved = unsolved
            unsolved = self.get_unsolved_count()

    # 遍历每一个 row/column/block ，如果 row/column/block 内唯一有一个空 cell 拥有某个候选数，这个空 cell 就可以 confirm 这个候选数
    def unique_nominee(self):
        previous_unsolved = None
        unsolved = self.get_unsolved_count()
        while(previous_unsolved != unsolved):
            for unit in ['row', 'column', 'block']:
                for num in range(9):
                    empty_cells = list(filter(lambda x: x.value == 0, self.get_cells_by(unit, num)))
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

    # 显/隐性数组：如果某个 row/column/block 中，有 m 个空 cell ，由其中 n(m>n) 个空 cell 的候选数组成的集合元素个数恰好为 n ，那么可以在另外的那 m-n 个空 cell 中去除这些候选数
    def number_chain(self, rank):
        for unit in ['row', 'column', 'block']:
            for num in range(9):
                empty_cells = list(filter(lambda x: x.value == 0, self.get_cells_by(unit, num)))
                # 有效的 n 链数只会出现在至少 n+1 个空 cell 的情况中
                if len(empty_cells) > rank:
                    combinations = itertools.combinations(empty_cells, rank)
                    for c in combinations:
                        combination_nominees = list(map(lambda x: x.nominees, c))
                        combination_nominees_set = set([x for y in combination_nominees for x in y])
                        if len(combination_nominees_set) == rank:
                            for other_empty in list(filter(lambda x: x not in c, empty_cells)):
                                for n in combination_nominees_set:
                                    if n in other_empty.nominees:
                                        self.cells[(other_empty.row, other_empty.column)].nominees.remove(n)

    # Y-wing
    def y_wing(self):
        for num in range(9):
            block = self.get_cells_by('block', num)
            doubles = list(filter(lambda x: len(x.nominees) == 2, block))
            double_group = list(itertools.combinations(doubles, 2))
            available_group = list(filter(lambda x: len(set(x[0].nominees) & set(x[1].nominees)) == 3 and x[0].row != x[1].row and x[0].column != x[1].column, double_group))
            if len(available_group) == 0:
                continue
            for ag in available_group:
                third_area = []
                third_area.append(self.get_cells_by('row', ag[0].row))
                third_area.append(self.get_cells_by('row', ag[1].row))
                third_area.append(self.get_cells_by('column', ag[0].column))
                third_area.append(self.get_cells_by('column', ag[1].column))
                third_area = list(filter(lambda x: x.block != num, third_area))
                for cell in third_area:
                    if set(cell.nominees) == set(ag[0].nominees) ^ set(ag[1].nominees):
                        if cell.row == ag[0].row or cell.column == ag[0].column:
                            nominee_to_delete = (set(cell.nominees) & set(ag[1].nominees)).pop()
                            inner_influence = [x for y in [self.get_cells_by('row', ag[1].row), self.get_cells_by('column', ag[1].column), self.get_cells_by('block', ag[1].block)] for x in y]
                            outer_influence = [x for y in [self.get_cells_by('row', cell.row), self.get_cells_by('column', cell.column), self.get_cells_by('block', cell.block)] for x in y]
                            common_influence = list(set(inner_influence) & set(outer_influence))
                            for ci in common_influence:
                                if nominee_to_delete in ci.nominees:
                                    self.cells[(ci.row, ci.column)].nominees.remove(nominee_set)
                        if cell.row == ag[1].row or cell.column == ag[1].column:
                            nominee_to_delete = (set(cell.nominees) & set(ag[0].nominees)).pop()
                            inner_influence = [x for y in [self.get_cells_by('row', ag[0].row), self.get_cells_by('column', ag[0].column), self.get_cells_by('block', ag[0].block)] for x in y]
                            outer_influence = [x for y in [self.get_cells_by('row', cell.row), self.get_cells_by('column', cell.column), self.get_cells_by('block', cell.block)] for x in y]
                            common_influence = list(set(inner_influence) & set(outer_influence))
                            for ci in common_influence:
                                if nominee_to_delete in ci.nominees:
                                    self.cells[(ci.row, ci.column)].nominees.remove(nominee_set)

    # 按照优先级，往复遍历一次所有求值方法
    def whole_solve(self):
        priority = [self.kill_nominees, self.unique_nominee]
        whole = priority[:-1] + priority[::-1]
        previous_unsolved = None
        unsolved = self.get_unsolved_count()
        while(previous_unsolved != unsolved):
            for method in whole:
                method()
            self.number_chain(2)
            self.number_chain(3)
            previous_unsolved = unsolved
            unsolved = self.get_unsolved_count()

    def show_nominees(self):
        for i in range(9):
            for j in range(9):
                print(self.cells[(i, j)].nominees, end=' ')
            print()

            
if __name__ == '__main__':
    s = Sudoku()
    s.read_sudoku('aaa')
    s.whole_solve()
    print()
    s.display_sudoku()
