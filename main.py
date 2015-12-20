# -*- coding: utf-8 -*-
# g.sorgente: sudoku main
# tests:
#       python main.py -n 3 -v 3,0,9,7,0,0,0,0,0,4,8,5,0,0,0,2,0,6,0,0,0,4,5,8,0,0,0,0,2,0,0,3,0,0,9,0,0,7,0,5,0,9,0,4,0,0,5,0,0,1,0,0,8,0,0,0,0,1,4,5,0,0,0,1,0,8,0,0,0,4,6,5,0,0,0,0,0,6,7,0,3 -a solve
import sys
import Cell
from Sudoku import Sudoku

if (len(sys.argv) <= 1):
    print("usage:")
    print("python main.py \n\
        -n (3|4)       : initialize an empty sudoku of the specified dimension \n\
        -v (values)    : list of values separated by comma \n\
        -a action      : do action \n\
        supported action: \n\
            * print: print in console the sudoku values \n\
            * solve: solve the sudoku \n\
            * generate: generate a new sudoku puzzle")


sudo = None

for arg in sys.argv[1::2]:
    idx = sys.argv.index(arg) + 1
    if len(sys.argv) <= idx:
        raise Exception("Specify a value for the action : " + arg)

    argvalue = sys.argv[idx]
    if arg == "-n":
        sudo = Sudoku(int(argvalue))

    if arg == "-v":
        index = 0
        cells_number = sudo.dimension ** 2
        for value in str(argvalue).split(","):
            x = index // cells_number
            y = index - ((index // cells_number) * cells_number)
            sudo.set_value(x, y, value)
            index += 1

    if arg == "-a":
        if argvalue == "print":
            sudo.print()
        if argvalue == "solve":
            sudo.print()
            sudo.solve()
            sudo.print()
        if argvalue == "generate":
            sudo.print()
            sudo.generate()
            sudo.print()
        else:
            raise Exception("Action not managed: " + argvalue)