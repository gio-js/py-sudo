# -*- coding: utf-8 -*-
# g.sorgente: sudoku container class
import Cell


class Sudoku:

    def __init__(self, dimension):
        self.dimension = dimension
        cells_per_row = self.dimension * self.dimension
        cells_number = cells_per_row ** 2
        self.cells = []

        print (cells_per_row)
        print (cells_number)
        for i in range(cells_number):
            self.cells.append(
                Cell.Cell(
                    i - ((i // cells_per_row) * cells_per_row),
                    i // cells_per_row,
                    0
                )
            )

    def echo(self):
        for cell in self.cells:
            print("{%i, %i, %s}" % (cell.x, cell.y, cell.value))


if __name__ == "__main__":
    sudo = Sudoku(3)
    sudo.echo()
    #dir(Cell.Cell)