from enum import auto, Enum


class Position(Enum):
    """
    Represents the state of a board position.
    """
    PLAYER1 = '1'
    PLAYER2 = '2'
    EMPTY = ' '
    FILLED = 'XXX'
