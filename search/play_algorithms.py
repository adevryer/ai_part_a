# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

import itertools
from queue import PriorityQueue
from .core import PlayerColor, Coord, Direction, PlaceAction, BOARD_N
from .placement_algorithms import find_starting_positions, find_all_placements, PlacementProblem
from .utils import render_board

PATH_COST = 4
LARGEST_DISTANCE = 2 * BOARD_N


class SearchProblem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, target):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.target = target

    def actions(self, state):
        possible_actions = []
        place_actions = []

        placement_positions = find_starting_positions(state)
        print(placement_positions)

        for position in placement_positions:
            #print(position)
            current_actions = find_all_placements(PlacementProblem(position, state))
            #print(current_actions)
            for element in current_actions:
                #print(f"Element: {element}")
                possible_actions.append(element)


        possible_actions = list(possible_actions for possible_actions, _ in itertools.groupby(possible_actions))
        #print(f"NO DUPLICATES: {possible_actions}")

        for element in possible_actions:
            place_actions.append(PlaceAction(element[0], element[1], element[2], element[3]))

        return place_actions

    def result(self, state, action: PlaceAction):
        new_state = state.copy()
        new_state[action.c1] = PlayerColor.RED
        new_state[action.c2] = PlayerColor.RED
        new_state[action.c3] = PlayerColor.RED
        new_state[action.c4] = PlayerColor.RED
        return new_state

    def heuristic(self, state):
        print("HI")
        #print(state)
        closest_distance = LARGEST_DISTANCE

        closest_positions = find_starting_positions(state)
        for coord in closest_positions:
            first = coord.__sub__(self.target)
            second = self.target.__sub__(coord)

            row_distance = min(first.r, second.r)
            col_distance = min(first.c, second.c)

            for i in range(0, BOARD_N):
                if Coord(i, self.target.c) not in state:
                    row_distance += 1

            for i in range(0, BOARD_N):
                if Coord(self.target.r, i) not in state:
                    col_distance += 1

            min_distance = min(row_distance, col_distance)

            if min(row_distance, col_distance) < closest_distance:
                closest_distance = min_distance

        return closest_distance

    def goal_test(self, state):
        row_success = True
        column_success = True

        for i in range(0, BOARD_N):
            if Coord(self.target.r, i) not in state:
                row_success = False
                break

        for i in range(0, BOARD_N):
            if Coord(i, self.target.c) not in state:
                column_success = False
                break

        if row_success or column_success:
            return True

        return False

    def path_cost(self, prev_cost):
        return prev_cost + PATH_COST


class SearchNode:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, problem, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.problem = problem
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0

    def expand(self):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(action)
                for action in self.problem.actions(self.state)]

    def child_node(self, action):
        next_state = self.problem.result(self.state, action)
        next_node = SearchNode(next_state, self.problem, self, action, self.problem.path_cost(self.path_cost))
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

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, SearchNode) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)