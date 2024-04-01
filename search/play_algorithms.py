# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

import itertools
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

from .core import PlayerColor, Coord, PlaceAction, BOARD_N
from .placement_algorithms import find_all_placements, PlacementProblem
from .helpers import dict_hash, find_gaps, find_starting_positions
from .utils import render_board

PATH_COST = 4
LARGEST_DISTANCE = 2 * BOARD_N


@dataclass(order=True)
class PrioritisedItem:
    """Class defining an entry in the priority queue which is only sorted based on priority. Adapted from the Python
    Standard Libray Queue documentation page."""
    priority: int
    heuristic_value: int = field(compare=False)
    item: Any = field(compare=False)


class SearchNode:
    """Node used when conducting A* search to find the optimal solution to the search problem. This code is adapted
    from the Node class in AIMA's Pyhton Library."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(action, problem) for action in problem.actions(self.state)]

    def child_node(self, action, problem):
        """Create child nodes of the parent node."""
        next_state = problem.result(self.state, action)
        next_node = SearchNode(next_state, self, action, problem.path_cost(self.path_cost))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return dict_hash(self.solution())


class SearchProblem:
    """The class for the optimal solution problem. Defines heuristics and allowed actions given the initial game
    state. Adapted from AIMA's Python library Problem class."""

    def __init__(self, initial, target):
        """The constructor specifies the initial board and the target coordinate."""
        self.initial = initial
        self.target = target

    def actions(self, state):
        """This class finds all possible placements of game pieces given the current board state."""
        possible_actions = []
        place_actions = []

        # Find squares which are adjacent to red blocks
        placement_positions = find_starting_positions(state)

        for position in placement_positions:
            current_actions = find_all_placements(PlacementProblem(position, state))
            for element in current_actions:
                possible_actions.append(element)

        # Remove any duplicate states from the list
        possible_actions = list(possible_actions for possible_actions, _ in itertools.groupby(possible_actions))

        # Turn these combinations into PlaceActions and return
        for element in possible_actions:
            place_actions.append(PlaceAction(element[0], element[1], element[2], element[3]))

        return place_actions

    def result(self, state, action: PlaceAction):
        """Creates the new board state after placing the new piece. Also checks if any lines were formed and will
        remove these squares if found."""
        new_state = state.copy()
        new_state[action.c1] = PlayerColor.RED
        new_state[action.c2] = PlayerColor.RED
        new_state[action.c3] = PlayerColor.RED
        new_state[action.c4] = PlayerColor.RED

        if not self.goal_test(new_state):
            # We need to check these rows and columns for any full lines
            rows = {action.c1.r, action.c2.r, action.c3.r, action.c4.r}
            cols = {action.c1.c, action.c2.c, action.c3.c, action.c4.c}

            row_duplicate = set()
            col_duplicate = set()

            for element in rows:
                duplicates = True

                for i in range(0, BOARD_N):
                    if Coord(element, i) not in new_state.keys():
                        duplicates = False

                if duplicates:
                    row_duplicate.add(element)

            for element in cols:
                duplicates = True

                for i in range(0, BOARD_N):
                    if Coord(i, element) not in new_state.keys():
                        duplicates = False

                if duplicates:
                    col_duplicate.add(element)

            # Remove the squares if we found duplicates
            for element in row_duplicate:
                for i in range(0, BOARD_N):
                    if Coord(element, i) in new_state.keys():
                        new_state.pop(Coord(element, i))

            for element in col_duplicate:
                for i in range(0, BOARD_N):
                    if Coord(i, element) in new_state.keys():
                        new_state.pop(Coord(i, element))

        return new_state

    def heuristic(self, state):
        """Defines the heuristic function used for A* search. The heuristic is modified from Manhattan distance:
        1. The heuristic finds the distance from the closest red square to the row/column where the target block
            is located.
        2. The heuristic then finds how many empty squares need to be filled in the row/column of the target coordinate
            to complete a full line.
        3. The heuristic adds a higher cost if there are smaller gaps in the row/column than for larger gaps. This is
            explained more in the helpers.py file."""

        row_distance = col_distance = LARGEST_DISTANCE

        for key, value in state.items():
            if value == PlayerColor.RED:
                first = key.__sub__(self.target)
                second = self.target.__sub__(key)

                # Find the minimum distance between the closest red square and the associated row/column
                # of the target coordinate
                curr_row_min = min(first.c - 1 if first.c > 0 else 0, second.c - 1 if second.c > 0 else 0)
                curr_col_min = min(first.r - 1 if first.r > 0 else 0, second.r - 1 if second.r > 0 else 0)

                if curr_row_min < row_distance:
                    row_distance = curr_row_min

                if curr_col_min < col_distance:
                    col_distance = curr_col_min

        # Calculate the cost of filling the row/column and return the minimum cost out of rows or columns
        fill_row, fill_col = find_gaps(state, self.target, row_distance, col_distance)
        return min(fill_row + row_distance, fill_col + col_distance)

    def goal_test(self, state):
        """Checks whether the specified state is a valid goal state."""
        row_success = column_success = True

        for i in range(0, BOARD_N):
            if Coord(self.target.r, i) not in state.keys():
                row_success = False
                break

        for i in range(0, BOARD_N):
            if Coord(i, self.target.c) not in state.keys():
                column_success = False
                break

        if row_success or column_success:
            return True

        return False

    def path_cost(self, prev_cost):
        return prev_cost + PATH_COST


def astar_search(problem):
    node_number = 1

    # Create an initial node for search and initialise a PQ for new nodes
    node = SearchNode(problem.initial)
    queue = PriorityQueue()
    heuristic = problem.heuristic(node.state)
    queue.put(PrioritisedItem(node.path_cost + heuristic, heuristic, node))
    seen = set()

    while not queue.empty():
        # Get the next item with the lowest cost from the queue
        retrieval = queue.get()
        node = retrieval.item
        print(f"NODE NUMBER: {node_number}")
        print(f"PRIORITY: {retrieval.priority}\n{render_board(node.state, problem.target, ansi=True)}")
        node_number += 1

        # Only check if it is a goal state if the value of the heuristic function is 0
        if retrieval.heuristic_value == 0:
            if problem.goal_test(node.state):
                return node

        # Expand the current state and add these children to the queue
        for child in node.expand(problem):
            curr_hash = child.__hash__()

            # Do not include nodes that we have already inserted into the PQ
            if curr_hash not in seen:
                heuristic = problem.heuristic(child.state)
                queue.put(PrioritisedItem(child.path_cost + heuristic, heuristic, child))
                seen.add(curr_hash)

    # Queue is empty and we have not found a solution, we cannot solve for the particular board state
    return None
