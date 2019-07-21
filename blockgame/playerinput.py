from enum import auto, Enum


class PlayerInput(Enum):
    """
    Represents the state of a board position.
    """
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    QUIT = 'Q'



