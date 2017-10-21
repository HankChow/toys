#!/usr/bin/env python3
# coding: utf-8

class Cell(object):
    
    def __init__(self, r, c, v=0):
        self.row = r
        self.column = c
        self.value = v
        self.nominees = [n for n in range(1, 10)]

    def confirm(self, v):
        self.value = v
        self.nominees = []

class Sudoku(object):

    def __init__(self):
        self.cells = {}
        for r in range(9):
            for c in range(9):
                cell = Cell(r, c)
                self.cells[(r, c)] = cell

    def read_quiz(self):
        pass
