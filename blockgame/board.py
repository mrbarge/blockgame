import random
from blockgame.position import Position


class Board(object):

    def __init__(self, size_x, size_y, units_per_side):
        # Board width can't be even, so increase it by one if it is
        if size_x % 2 == 0:
            size_x += 1
        self.width = size_x
        self.height = size_y
        self._generate_board(self.width, self.height, units_per_side)

    def _generate_board(self, width, height, units_per_side):
        self._board = [[Position.EMPTY] * width for i in range(height)]

        # populate players
        for i in range(0, units_per_side):
            lx, ly = self._find_free_pos()
            rx, ry = self._find_free_pos(right_side=True)
            self._board[ly][lx] = Position.PLAYER1
            self._board[ry][rx] = Position.PLAYER2

        # populate blocks fairly, randomized on each side
        # to be fair, each side should have the same quantity, at least 50%
        max_blocks_per_side = int((len(self._board) * int(self.width / 2) - units_per_side) / 2)
        for i in range(0, max_blocks_per_side):
            lx, ly = self._find_free_pos()
            rx, ry = self._find_free_pos(right_side=True)
            self._board[ly][lx] = Position.FILLED
            self._board[ry][rx] = Position.FILLED

        # Now randomly populate the middle column
        mid = int(width / 2)
        for y in range(0, height):
            self._board[y][mid] = Position.FILLED if random.choice([True, False]) else Position.EMPTY

        # a column should not be entirely blocks
        for x in range(width):
            if self._is_filled_column(x):
                # just clear out the top position
                self._board[0][x] = Position.EMPTY

        # let units settle into place

    def _find_free_pos(self, right_side=False):
        """
        Find a free empty position on a player's side in which to place an object.
        :param right_side: Look in player2's space instead of player1's.
        :return:
        """
        found = False
        player_x_space = int(self.width / 2)
        player_y_space = self.height
        while not found:
            x = random.randint(0, player_x_space - 1)
            x = len(self._board[0]) - x - 1 if right_side else x
            y = random.randint(0, player_y_space - 1)

            if self._board[y][x] == Position.EMPTY:
                return x, y

    def _is_filled_column(self, x):
        """
        Check if a column is entirely full of non-empty objects.
        :param x: index of column (starting at 0)
        :return: true if column is full
        """
        filled_cols = [True for y in range(self.height) if self._board[y][x] == Position.FILLED]
        return filled_cols.count(True) == self.height

    def _shift_column_down(self, x):
        """
        Shift a column downwards.
        The lower-most element is sent to the top.
        :param x: index of column (starting at 0)
        :return:
        """
        max_y = self.height - 1
        tmp = self._board[max_y][x]
        for y in reversed(range(1, max_y + 1)):
            self._board[y][x] = self._board[y - 1][x]
        self._board[0][x] = tmp

    def _shift_column_up(self, x):
        """
        Shift a column upwards.
        The upper-most element is sent to the bottom.
        :param x: index of column (starting at 0)
        :return:
        """
        max_y = self.height - 1
        tmp = self._board[0][x]
        for y in range(max_y):
            self._board[y][x] = self._board[y + 1][x]
        self._board[max_y][x] = tmp

    def _apply_gravity(self):
        """
        Let all players fall to a resting point if they're currently floating
        """
        for y in range(self.height - 2):  # don't need to check bottom row
            for x in range(self.width):
                if (Board._is_player(self._board[y][x]) and
                        self._board[y + 1][x] == Position.EMPTY):
                    self._board[y + 1][x] = self._board[y][x]
                    self._board[y][x] = Position.EMPTY

    def print(self):
        """
        Print the board state.
        :return:
        """
        for y in range(self.height):
            xv = [x.value for x in self._board[y]]
            print('|'.join(xv))
            print('-' * (self.width * 2 - 1))

    @staticmethod
    def no_moves_left(board):
        """
        Check if there are any possible movements a player object can do
        :return:
        """
        for y in range(len(board)):  # don't need to check bottom row
            for x in range(len(board[0])):
                # can player1 move right?
                if (x + 1 < len(board[0]) and
                        board[y][x] == Position.PLAYER1 and
                        board[y][x + 1] == Position.EMPTY):
                    return False

                # can player2 move left?
                if (x - 1 >= 0 and
                        board[y][x] == Position.PLAYER2 and
                        board[y][x - 1] == Position.EMPTY):
                    return False
        return True

    @staticmethod
    def _is_player(p):
        """
        Check if the supplied position is a player object.
        :param p:
        :return:
        """
        return isinstance(p, Position) and (p == Position.PLAYER1 or p == Position.PLAYER2)
