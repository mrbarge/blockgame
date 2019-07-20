import pytest
from collections import deque
from blockgame.board import Board
from blockgame.position import Position
from blockgame.match import Match


@pytest.fixture
def sample_board_medium_move():
    b = Board(5, 5, 3)
    b._board = [[Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.PLAYER2, Position.EMPTY],
                [Position.FILLED, Position.FILLED, Position.EMPTY, Position.FILLED, Position.PLAYER2],
                [Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.FILLED, Position.EMPTY],
                [Position.FILLED, Position.PLAYER1, Position.PLAYER1, Position.PLAYER2, Position.FILLED],
                [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED]]
    return b


@pytest.mark.usefixtures("sample_board_medium_move")
def test_get_valid_columns(sample_board_medium_move):
    m = Match(5, 5, 3)
    m._board = sample_board_medium_move
    m._turn = Position.PLAYER1

    cols = m.get_valid_columns()
    assert cols == [0, 1, 2]

    m._turn = Position.PLAYER2
    cols = m.get_valid_columns()
    assert cols == [3, 4]

    print(cols)


@pytest.mark.usefixtures("sample_board_medium_move")
def test_get_valid_columns_max_turns_reached(sample_board_medium_move):
    m = Match(5, 5, 3)
    m._board = sample_board_medium_move
    m._turn = Position.PLAYER1

    # test column remove when max used
    m._p1_columns = deque(Match.MAX_TURNS_FOR_COLUMN * [0], Match.MAX_TURNS_FOR_COLUMN)
    cols = m.get_valid_columns()
    assert cols == [1, 2]

    # test no removal when not max used
    m._p1_columns = deque((Match.MAX_TURNS_FOR_COLUMN-1) * [0], Match.MAX_TURNS_FOR_COLUMN)
    cols = m.get_valid_columns()
    assert cols == [0, 1, 2]

    # same as for player 2
    m._turn = Position.PLAYER2
    m._p2_columns = deque(Match.MAX_TURNS_FOR_COLUMN * [3], Match.MAX_TURNS_FOR_COLUMN)
    cols = m.get_valid_columns()
    assert cols == [4]

    # same as for player 2 when not max used
    m._turn = Position.PLAYER2
    m._p2_columns = deque((Match.MAX_TURNS_FOR_COLUMN-1) * [3], Match.MAX_TURNS_FOR_COLUMN)
    cols = m.get_valid_columns()
    assert cols == [3, 4]
