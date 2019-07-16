import random
from blockgame.position import Position


class Board(object):

    def __init__(self, size_x, size_y, units_per_side):
        # Board width can't be even, so increase it by one if it is
        if size_x % 2 == 0:
            size_x += 1
        self.width = size_x
        self.height = size_y
        self._player1_score = 0
        self._player2_score = 0
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
        # Keep on applying gravity until no more players move
        unit_moved = True
        while unit_moved:
            unit_moved = False
            for y in range(self.height):  # don't need to check bottom row
                for x in range(self.width):
                    if (Board._is_player(self._board[y][x]) and
                            Board.can_move_down(self._board, x, y)):
                        self._board[y + 1][x] = self._board[y][x]
                        self._board[y][x] = Position.EMPTY
                        unit_moved = True

    def _move_player(self, player):
        """
        A dumb version of move player. All of a player's units move 1 square
        in each turn (if they can).
        :param player:
        :return:
        """
        if not isinstance(player, Position):
            raise Exception("Invalid input type for player")

        while not Board.no_moves_left(self._board, player):
            for y in range(self.height):
                for x in range(self.width):

                    if not self._is_player(self._board[y][x]):
                        continue

                    elif player == Position.PLAYER1 and Board.can_move_right(self._board, x, y):
                        self._board[y][x] = Position.EMPTY
                        # is this a scoring move?
                        if x + 2 == self.width:
                            # yes, increase score
                            self._player1_score += 1
                        else:
                            # no, move the player along
                            self._board[y][x + 1] = Position.PLAYER1

                    elif player == Position.PLAYER2 and Board.can_move_left(self._board, x, y):
                        self._board[y][x] = Position.EMPTY
                        # is this a scoring move?
                        if x - 1 == 0:
                            # yes, increase score
                            self._player2_score += 1
                        else:
                            # no, move the player along
                            self._board[y][x - 1] = Position.PLAYER2

                    # apply gravity before evaluating the next position
                    self._apply_gravity()

    def _move_player_new(self, starting_column, player):
        """
        A better version of move player.
        Pick a starting column, and move any player pieces found to
        their eventual final destination before considering moving
        any other pieces.
        :param starting_column: column to start at (and move backwards from)
        :param player:
        :return:
        """
        if not isinstance(player, Position):
            raise Exception("Invalid input type for player")

        if player == Position.PLAYER1:
            for x in reversed(range(starting_column + 1)):
                for y in range(self.height):
                    if self._board[y][x] != Position.PLAYER1:
                        continue

                    if Board.can_move_right(self._board, x, y):
                        self._move_piece(x, y, move_right=True)

                    self._apply_gravity()

        else:
            for x in range(starting_column, self.width):
                for y in range(self.height):
                    if self._board[y][x] != Position.PLAYER2:
                        continue

                    if Board.can_move_left(self._board, x, y):
                        self._move_piece(x, y, move_right=False)

                    self._apply_gravity()

    def _move_piece(self, x, y, move_right=True):
        """
        Move a piece until it can't move anymore
        :param x: starting x pos
        :param y: starting y pos
        :return: True if the piece reaches the end, counts as point
        """

        finished_moving = False
        player = self._board[y][x]
        while not finished_moving:
            if self.can_move_right():
                self._board[y][x] = Position.EMPTY
                if Board.scoring_move():
                    return True
                else:
                    if move_right:
                        self._board[y][x + 1] = player
                    else:
                        self._board[y][x - 1] = player

            elif self.can_move_down():
                self._board[y][x] = Position.EMPTY
                self._board[y + 1][x] = player

            else:
                finished_moving = True

        return False

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
    def no_moves_left(board, player):
        """
        Check if there are any possible movements a player object can do
        :return:
        """
        if not isinstance(player, Position):
            raise Exception("Invalid input type for player")

        for y in range(len(board)):  # don't need to check bottom row
            for x in range(len(board[0])):
                if (player == Position.PLAYER1 and
                        Board._is_player(board[y][x]) and
                        (Board.can_move_right(board, x, y) or Board.can_move_down(board, x, y))
                ):
                    return False
                if (player == Position.PLAYER2 and
                        Board._is_player(board[y][x]) and
                        (Board.can_move_left(board, x, y) or Board.can_move_down(board, x, y))
                ):
                    return False
        return True

    def score(self):
        return (self._player1_score, self._player2_score)

    @staticmethod
    def can_move_left(board, x, y):
        return (x - 1 >= 0 and board[y][x - 1] == Position.EMPTY)

    @staticmethod
    def can_move_right(board, x, y):
        return (x + 1 < len(board[0]) and board[y][x + 1] == Position.EMPTY)

    @staticmethod
    def can_move_down(board, x, y):
        return (y + 1 < len(board) and board[y + 1][x] == Position.EMPTY)

    @staticmethod
    def scoring_move(board, x):
        return (x < 0 or x >= len(board[0]))

    @staticmethod
    def _is_player(p):
        """
        Check if the supplied position is a player object.
        :param p:
        :return:
        """
        return isinstance(p, Position) and (p == Position.PLAYER1 or p == Position.PLAYER2)
