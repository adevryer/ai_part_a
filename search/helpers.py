import functools
from .core import Coord, PlayerColor, BOARD_N


def dict_hash(solution):
    coords = []

    for element in solution:
        coords.append((element.c1.r, element.c1.c))
        coords.append((element.c2.r, element.c2.c))
        coords.append((element.c3.r, element.c3.c))
        coords.append((element.c4.r, element.c4.c))

    coords.sort()
    hash_val = ''

    for element in coords:
        hash_val += str(element[0])
        hash_val += str(element[1])

    return hash_val