# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

import itertools
from .core import PlayerColor, Coord, PlaceAction
from .utils import render_board
from .placement_algorithms import find_starting_positions, find_all_placements, PlacementProblem
from .play_algorithms import SearchProblem, SearchNode


def search(
    board: dict[Coord, PlayerColor], 
    target: Coord
) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    """
    positions = find_starting_positions(board)
    print(f"COULD START AT {positions}")

    for position in positions:
        print()
        print(f"NEW POSITION STARTING NOW: {position}")
        find_all_placements(PlacementProblem(position, board))
    """

    """
    possible_actions = []
    placement_positions = find_starting_positions(board)
    for position in placement_positions:
        possible_actions += find_all_placements(PlacementProblem(position, board))

    possible_actions = list(possible_actions for possible_actions, _ in itertools.groupby(possible_actions))

    print("POSSIBLE:")
    for element in possible_actions:
        print(PlaceAction(element[0], element[1], element[2], element[3]))

    #print(target)
    """

    print(PlaceAction(Coord(0,1), Coord(0,2), Coord(1,2), Coord(2,2)))
    problem = SearchProblem(board, target)
    actions = problem.actions(board)
    new_map = problem.result(board, actions[10])

    print(render_board(new_map, target, ansi=True))

    """
    print(f"CHECK HERE: {Coord(1, 0).__sub__(target)}")
    print(f"CHECK HERE: {target.__sub__(Coord(1, 0))}")
    """

    print(render_board(board, target, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
        PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
        PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    ]
