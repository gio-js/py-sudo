# -*- coding: utf-8 -*-
# g.sorgente: sudoku cell class


class Cell:

    def __init__(self, x, y, value, sudoku_dimension):
        self.x = x
        self.y = y
        self.value = value
        self.available_solutions = []  # managed by Sudoku class
        self.qx = (x // sudoku_dimension)
        self.qy = (y // sudoku_dimension)
        self.qindex = self.qx + (self.qy * sudoku_dimension)