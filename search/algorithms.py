from .core import PlayerColor, Coord, Direction

SEARCH_LIMIT = 4


def find_starting_positions(board: dict[Coord, PlayerColor]):
    """ Finds the possible locations where pieces can be placed given the current board state """
    player_pieces = []
    starting_positions = []

    for coord, color in board.items():
        if color == PlayerColor.RED:
            player_pieces.append(coord)

    for coord in player_pieces:
        possible_positions = [coord.__add__(Direction.Up), coord.__add__(Direction.Down), coord.__add__(Direction.Left),
                              coord.__add__(Direction.Right)]

        for element in possible_positions:
            if element not in board:
                starting_positions.append(element)

    return starting_positions


def find_all_placements(problem, limit=SEARCH_LIMIT):
    """ Adapted from AIMA's Python Library function for depth-limited search """
    placements = []

    def recursive_dls(node, curr_problem, curr_limit):
        if curr_limit == 1:
            new_path = sorted(node.path())
            if new_path not in placements:
                placements.append(new_path)

        else:
            for child in node.expand(curr_problem):
                if child not in node.path():
                    recursive_dls(child, curr_problem, curr_limit - 1)

    # Body of depth_limited_search:
    recursive_dls(Node(problem.initial, None), problem, limit)
    print(f"FINAL: {sorted(placements)}")
    return placements


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.depth = self.parent.depth + 1 if parent else 0

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        print(f"PATH = {self.path()}")
        return [self.child_node(next_state)
                for next_state in problem.actions(self.state, self.path())]

    def child_node(self, next_state):
        """[Figure 3.10]"""
        next_node = Node(next_state, self)
        return next_node

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node.state)
            node = node.parent
        return list(reversed(path_back))


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, current_map):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.current_map = current_map

    def actions(self, state, last_moves):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # pieces can be placed in four possible directions on the gameboard
        possible_moves = [state.__add__(Direction.Up), state.__add__(Direction.Down), state.__add__(Direction.Left),
                          state.__add__(Direction.Right)]

        for element in last_moves:
            if element is not state:
                possible_moves.append(element.__add__(Direction.Up))
                possible_moves.append(element.__add__(Direction.Down))
                possible_moves.append(element.__add__(Direction.Left))
                possible_moves.append(element.__add__(Direction.Right))

        # cannot be placed if a piece is already taking that space
        possible_moves = [element for element in possible_moves if element not in self.current_map]

        # cannot be placed if we have already placed a piece there during this iteration of piece forming
        possible_moves = [element for element in possible_moves if element not in last_moves]

        print(f"ELEMENTS: {possible_moves}")
        return possible_moves
