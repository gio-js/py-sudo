# -*- coding: utf-8 -*-
# g.sorgente: sudoku container class
import random
import copy
import Cell


class Sudoku:
    NO_VALUE = 0

    def __init__(self, dimension):
        """Sudoku constructor"""
        self.dimension = dimension
        self.cells = []

        # generate cells
        cells_per_row = self.dimension ** 2
        cells_number = cells_per_row ** 2
        for i in range(cells_number):
            self.cells.append(
                Cell.Cell(
                    i // cells_per_row,
                    i - ((i // cells_per_row) * cells_per_row),
                    Sudoku.NO_VALUE,
                    self.dimension
                )
            )

    def print(self):
        """Output in console current sudoku"""
        cells_number = self.dimension ** 2
        grid = ""
        for x in range(cells_number):
            grid += " \n"
            for y in range(cells_number):
                cell = self._get_cell(x, y)
                grid += " {0:02d}".format(cell.value)
        print(grid)

    @property
    def solved(self):
        """Returns true if there aren't any cells without a valid solution"""
        return len(self._not_solved_cells()) == 0

    def solve(self):
        """Solve sudoku"""
        return self._solve_internal()

    def set_value(self, x, y, value):
        """Set cell value"""
        self._get_cell(x, y).value = int(value)

    def generate(self):
        """Generate a new sudoku scheme"""
        cells_to_fill = {
            2: random.randint(2, 6),
            3: random.randint(8, 10),
            4: random.randint(30, 40),
            5: random.randint(100, 120)
        }

        # 1. fill a random amount of cells
        for i in range(cells_to_fill[self.dimension]):
            x = random.randint(0, self.dimension ** 2 - 1)
            y = random.randint(0, self.dimension ** 2 - 1)
            value = random.randint(1, self.dimension ** 2)

            cell = self._get_cell(x, y)
            # if it's not an empty cell or that cell can not contain the random value, then pick another cell
            if (cell.value != Sudoku.NO_VALUE or not self._cell_can_contain(x, y, value)):
                i -= 1
            else:
                cell.value = value

        # 2. solve the puzzle
        self._solve_internal()

        # 3. empty some cells, and serve the puzzle

    def clear(self):
        """Clear all the cells setting NO_VALUE"""
        for cell in self.cells:
            cell.value = Sudoku.NO_VALUE

    # private methods
    def _solve_internal(self):
        """Solve sudoku"""
        self._build_available_solutions()

        # get remaining cells to solve
        not_solved_cells = self._not_solved_cells()

        for cell in not_solved_cells:  # per each cell
            if len(cell.available_solutions) == 1:  # only one available solution
                cell.value = cell.available_solutions[0]
            else:  # get solution merging solutions with linked cells
                solution_neighbours = self._get_first_solution_by_neighbours(cell)
                if solution_neighbours is not None:
                    cell.value = solution_neighbours

                    # a valid solution have been found, go ahead and recalculate avaliable
                    # solution on the entire grid
                    not_solved_cells = self._not_solved_cells()
                    self._build_available_solutions()
                    continue

        # 1. check, is it solved?
        if self.solved:
            return True

        # 2. check, is there any empty cells that can not contain any value (available_solutions == 0)
        empty_cells = [cell for cell in self._not_solved_cells() if len(cell.available_solutions) == 0]
        if len(empty_cells) > 0:
            return False

        # our solution strategies failed, we keep randomly one value from
        # available_solutions for an empty cell and we continue solving operation
        first_cell = None
        for cell in self._not_solved_cells():
            if first_cell is None or \
               len(cell.available_solutions) < len(first_cell.available_solutions):
                first_cell = cell

        # let's continue with solving, first of all, we create a deep clone of the cells
        cells_clone = copy.deepcopy(self.cells)
        available_solution_clone = copy.copy(first_cell.available_solutions)
        cell_x = first_cell.x
        cell_y = first_cell.y

        for solution_value in available_solution_clone:
            first_cell.value = solution_value

            # recoursive call
            if self._solve_internal() is True:
                return True

            # otherwise we keep trying another solution, but first we restore the old
            # "revision" of cells and first_cell
            self.cells = copy.deepcopy(cells_clone)
            first_cell = self._get_cell(cell_x, cell_y)

    def _get_cell(self, x, y):
        """Get a specific cell by grid coordinates"""
        return [cell for cell in self.cells if cell.x == x and cell.y == y][0]

    def _cell_can_contain(self, x, y, value):
        """Checks wether a cell in the same row/column or quadrant has yet that value"""
        dummy_cell = Cell.Cell(x, y, value, self.dimension)
        found_cells = [cell for cell in self.cells
                       if (cell.x == dummy_cell.x or
                           cell.y == dummy_cell.y or
                           cell.qindex == dummy_cell.qindex) and
                           cell.value == dummy_cell.value]

        return len(found_cells) == 0

    def _not_solved_cells(self):
        """Get grid cells  specified that are still without a valid solution"""
        return [cell for cell in self.cells if cell.value == Sudoku.NO_VALUE]

    def _linked_cells(self, current_cell):
        """Get grid cells related (for the solution) to the specified one"""
        return [cell for cell in self.cells
                if cell is not current_cell and (
                    cell.x == current_cell.x or
                    cell.y == current_cell.y or
                    cell.qindex == current_cell.qindex)]

    def _build_available_solutions(self):
        """Check and build the available solutions for the grid cells"""
        for cell in self.cells:
            cell.available_solutions.clear()

            if cell.value != Sudoku.NO_VALUE:
                continue

            for v in range(self.dimension ** 2):
                cell.available_solutions.append(v + 1)

            linkedcells = self._linked_cells(cell)
            for linkedcell in linkedcells:
                if linkedcell.value in cell.available_solutions:
                    cell.available_solutions.remove(linkedcell.value)

    def _get_first_solution_by_neighbours(self, cell):
        """Merge available solutions of every dependant cell in order to get the first
        occurrence among valid solution"""
        linkedcells = self._linked_cells(cell)

        solutionsx = cell.available_solutions[:]
        solutionsy = cell.available_solutions[:]
        solutionsq = cell.available_solutions[:]

        for linkedcell in linkedcells:
            if linkedcell.x == cell.x:
                [solutionsx.remove(v) for v in linkedcell.available_solutions if v in solutionsx]

            if linkedcell.y == cell.y:
                [solutionsy.remove(v) for v in linkedcell.available_solutions if v in solutionsy]

            if linkedcell.qindex == cell.qindex:
                [solutionsq.remove(v) for v in linkedcell.available_solutions if v in solutionsq]

            if len(solutionsx) + len(solutionsy) + len(solutionsq) == 0:
                return None

        if len(solutionsx) == 1:
            return solutionsx[0]
        if len(solutionsy) == 1:
            return solutionsy[0]
        if len(solutionsq) == 1:
            return solutionsq[0]

        return None
