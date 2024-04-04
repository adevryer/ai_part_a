# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import Coord, PlayerColor, Direction

PIECE_SIZE = 4


def find_starting_positions(board: dict[Coord, PlayerColor]):
    """ Finds the possible locations where pieces can be placed given the current board state """
    player_pieces = []
    starting_positions = []

    # Find all red pieces currently on the board
    for coord, color in board.items():
        if color == PlayerColor.RED:
            player_pieces.append(coord)

    for coord in player_pieces:
        # We can place new squares in these four directions
        possible_positions = [coord + Direction.Up, coord + Direction.Down, coord + Direction.Left,
                              coord + Direction.Right]

        for element in possible_positions:
            if element not in board:
                starting_positions.append(element)

    return starting_positions


def dict_hash(solution):
    """Creates a "hash" of the current state map consisting of an integer which indicates the PlaceActions which have
    been used to reach the current board state. Used for quick comparisons for duplicates in A* search."""
    coords = []

    for element in solution:
        # Add all coordinates where we've placed new squares
        coords.append((element.c1.r, element.c1.c))
        coords.append((element.c2.r, element.c2.c))
        coords.append((element.c3.r, element.c3.c))
        coords.append((element.c4.r, element.c4.c))

    coords.sort()
    hash_val = '1'

    # Add these sorted coordinates to the "hash" and return
    for element in coords:
        hash_val += str(element[0])
        hash_val += str(element[1])

    return int(hash_val)


def find_gaps(board: dict[Coord, PlayerColor], target: Coord, row_dist: int, col_dist: int):
    """Helper function for the heuristic used for search. Helps find the cost to fill the row/column where the target
    coordinate is located."""
    init_coord = Coord(target.r, target.c)
    empty_spaces = 0
    row_gaps = []
    col_gaps = []
    row_cost = 0
    col_cost = 0
    first = True

    while init_coord.r != target.r or first:
        # Move down the current column by one each time
        first = False
        init_coord = init_coord + Direction.Down
        if init_coord not in board.keys():
            # We have found an empty space, record its length
            empty_spaces += 1
        else:
            if empty_spaces != 0:
                # We have reached the end of the empty space, add its final length to the list
                row_gaps.append(empty_spaces)
                empty_spaces = 0

    # Repeat the above process for the row of the target coordinate
    first = True
    while init_coord.c != target.c or first:
        first = False
        init_coord = init_coord + Direction.Right
        if init_coord not in board.keys():
            empty_spaces += 1
        else:
            if empty_spaces != 0:
                col_gaps.append(empty_spaces)
                empty_spaces = 0

    for element in row_gaps:
        # Current gap is larger than the size of a piece, add the gap size to the cost to fill the row
        if element >= PIECE_SIZE:
            row_cost += element
        else:
            # If we can possibly fill this row by connecting it to the closest red block to the target column,
            # just add the size of the gap to the cost to fill the row as we have already factored in filling the
            # gap between the closest red square and the target row previously
            if element + row_dist == PIECE_SIZE:
                row_cost += element
            else:
                # We would have to place a completely new piece to fill this gap, add the size of a piece (4) to the
                # cost to fill the row
                row_cost += PIECE_SIZE

    # Repeat the same for the column gaps
    for element in col_gaps:
        if element >= PIECE_SIZE:
            col_cost += element
        else:
            if element + col_dist == PIECE_SIZE:
                col_cost += element
            else:
                col_cost += PIECE_SIZE

    return row_cost, col_cost
