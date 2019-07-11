import random
from blockgame.position import Position


class Board(object):

    def __init__(self, size_x, size_y, units_per_side):
        # Board width can't be even, so increase it by one if it is
        if size_x % 2 == 0:
            size_x += 1
        self._generate_board(size_x, size_y, units_per_side)

    def _generate_board(self, size_x, size_y, units_per_side):
        self._board = [[Position.EMPTY] * size_x for i in range(size_y)]

        # populate players
        for i in range(0, units_per_side):
            lx, ly = self._find_free_pos()
            rx, ry = self._find_free_pos(right_side=True)
            self._board[ly][lx] = Position.PLAYER1
            self._board[ry][rx] = Position.PLAYER2

        # populate blocks fairly, randomized on each side
        # to be fair, each side should have the same quantity, at least 50%
        max_blocks_per_side = int ((len(self._board) * int(size_x / 2) - units_per_side)/2)
        for i in range(0, max_blocks_per_side):
            lx, ly = self._find_free_pos()
            rx, ry = self._find_free_pos(right_side=True)
            self._board[ly][lx] = Position.FILLED
            self._board[ry][rx] = Position.FILLED

        # Now randomly populate the middle column
        mid = int(size_x / 2)
        for y in range(0, len(self._board)):
            self._board[y][mid] = Position.FILLED if random.choice([True, False]) else Position.EMPTY

        # a column should not be entirely blocks
        for x in range(size_x):
            if self._is_filled_column(x):
                # just clear out the top position
                self._board[0][x] = Position.EMPTY

        # let units settle into place

    def _find_free_pos(self, right_side=False):
        found = False
        player_x_space = int(len(self._board[0]) / 2)
        player_y_space = len(self._board)
        while not found:
            x = random.randint(0, player_x_space-1)
            x = len(self._board[0]) - x - 1 if right_side else x
            y = random.randint(0, player_y_space-1)

            if self._board[y][x] == Position.EMPTY:
                return x, y

    def _is_filled_column(self, x):
        filled_cols = [True for y in range(len(self._board)) if self._board[y][x] == Position.FILLED]
        return filled_cols.count(True) == len(self._board)

    def _shift_column_down(self, x):
        max_y = len(self._board) - 1
        tmp = self._board[max_y][x]
        for y in reversed(range(1, max_y+1)):
            self._board[y][x] = self._board[y-1][x]
        self._board[0][x] = tmp

    def _shift_column_up(self, x):
        max_y = len(self._board) - 1
        tmp = self._board[0][x]
        for y in range(max_y):
            self._board[y][x] = self._board[y+1][x]
        self._board[max_y][x] = tmp

    def print(self):
        for y in range(len(self._board)):
            xv = [x.value for x in self._board[y]]
            print('|'.join(xv))
            print('-' * (len(self._board[y]) * 2 - 1))
