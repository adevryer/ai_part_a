from .core import Coord, PlayerColor, Direction
from .utils import render_board

PIECE_SIZE = 4

def dict_hash(solution):
    coords = []

    for element in solution:
        coords.append((element.c1.r, element.c1.c))
        coords.append((element.c2.r, element.c2.c))
        coords.append((element.c3.r, element.c3.c))
        coords.append((element.c4.r, element.c4.c))

    coords.sort()
    hash_val = '1'

    for element in coords:
        hash_val += str(element[0])
        hash_val += str(element[1])

    return hash_val


def find_gaps(board: dict[Coord, PlayerColor], target: Coord, row_dist: int, col_dist: int):
    init_coord = Coord(target.r, target.c)
    empty_spaces = 0
    row_gaps = []
    col_gaps = []
    row_cost = 0
    col_cost = 0
    first = True

    #print(render_board(board, target, ansi = True))

    while init_coord.r != target.r or first:
        first = False
        init_coord = init_coord.__add__(Direction.Down)
        if init_coord not in board.keys():
            empty_spaces += 1
        else:
            if empty_spaces != 0:
                row_gaps.append(empty_spaces)
                #print(f"Gap of {empty_spaces} found ROW")
                empty_spaces = 0

    first = True
    while init_coord.c != target.c or first:
        first = False
        init_coord = init_coord.__add__(Direction.Right)
        if init_coord not in board.keys():
            empty_spaces += 1
        else:
            if empty_spaces != 0:
                col_gaps.append(empty_spaces)
                #print(f"Gap of {empty_spaces} found COL")
                empty_spaces = 0

    #print(row_gaps, col_gaps)

    for element in row_gaps:
        if element >= PIECE_SIZE:
            row_cost += element
        else:
            if element + row_dist == PIECE_SIZE:
                row_cost += element
            else:
                row_cost += PIECE_SIZE

    for element in col_gaps:
        if element >= PIECE_SIZE:
            col_cost += element
        else:
            if element + col_dist == PIECE_SIZE:
                col_cost += element
            else:
                col_cost += PIECE_SIZE

    return row_cost, col_cost
