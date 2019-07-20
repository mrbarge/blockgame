from blockgame.board import Board
from blockgame.position import Position
from collections import deque
import random


class Match(object):
    # A column can only be moved this many times in a row before being disabled
    MAX_TURNS_FOR_COLUMN = 6

    def __init__(self, width, height, units_per_side):
        self._board = Board(width, height, units_per_side)
        self._player1_score = 0
        self._player2_score = 0
        self._p1_columns = deque([], self.MAX_TURNS_FOR_COLUMN)
        self._p2_columns = deque([], self.MAX_TURNS_FOR_COLUMN)
        self._turn = Match._decide_first_turn()

    @staticmethod
    def _decide_first_turn():
        """
        Decide and return which player gets the first turn.
        :param self:
        :return:
        """
        return Position.PLAYER1 if random.randint(0, 1) == 0 else Position.PLAYER2

    def get_valid_columns(self):
        """
        Determine the available moves that the current-turn player can make
        :return: List of movable columns (starting at 0)
        """

        cols = self._board.player_columns(self._turn)

        # remove a column if it has been picked the last X times
        if self._reached_column_max():
            if self._turn == Position.PLAYER1:
                cols.remove(self._p1_columns[0])
            else:
                cols.remove(self._p2_columns[0])

        return cols

    def _reached_column_max(self):
        """
        Determine if a player has moved the same column too many times in a row.
        :return:
        """
        if self._turn == Position.PLAYER1:
            return (len(self._p1_columns) == Match.MAX_TURNS_FOR_COLUMN and
                    all(e == self._p1_columns[0] for e in self._p1_columns))
        elif self._turn == Position.PLAYER2:
            return (len(self._p2_columns) == Match.MAX_TURNS_FOR_COLUMN and
                    all(e == self._p2_columns[0] for e in self._p2_columns))
