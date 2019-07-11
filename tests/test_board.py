import pytest
from blockgame.board import Board
from blockgame.position import Position


@pytest.fixture
def sample_board_medium():
    b = Board(5, 5, 3)
    b._board = [[Position.EMPTY, Position.FILLED, Position.FILLED, Position.PLAYER2, Position.EMPTY],
                [Position.PLAYER1, Position.FILLED, Position.EMPTY, Position.EMPTY, Position.PLAYER2],
                [Position.EMPTY, Position.FILLED, Position.FILLED, Position.PLAYER2, Position.EMPTY],
                [Position.FILLED, Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.FILLED],
                [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED]]
    return b

@pytest.fixture
def sample_board_small():
    b = Board(3, 3, 3)
    b._board = [[Position.FILLED, Position.EMPTY, Position.FILLED],
                [Position.FILLED, Position.EMPTY, Position.EMPTY],
                [Position.FILLED, Position.EMPTY, Position.FILLED],
                [Position.FILLED, Position.EMPTY, Position.EMPTY],
                [Position.FILLED, Position.EMPTY, Position.FILLED]]
    return b

@pytest.mark.usefixtures("sample_board_small")
def test_is_filled_column(sample_board_small):
    assert sample_board_small._is_filled_column(0) == True
    assert sample_board_small._is_filled_column(1) == False
    assert sample_board_small._is_filled_column(2) == False


@pytest.mark.usefixtures("sample_board_medium")
def test_shift_column_up(sample_board_medium):
    for x in range(5):
        sample_board_medium._shift_column_up(x)
    assert sample_board_medium._board == [
        [Position.PLAYER1, Position.FILLED, Position.EMPTY, Position.EMPTY, Position.PLAYER2],
        [Position.EMPTY, Position.FILLED, Position.FILLED, Position.PLAYER2, Position.EMPTY],
        [Position.FILLED, Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.FILLED],
        [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED],
        [Position.EMPTY, Position.FILLED, Position.FILLED, Position.PLAYER2, Position.EMPTY]
    ]


@pytest.mark.usefixtures("sample_board_medium")
def test_shift_column_down(sample_board_medium):
    for x in range(5):
        sample_board_medium._shift_column_down(x)
    assert sample_board_medium._board == [
         [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED],
         [Position.EMPTY, Position.FILLED, Position.FILLED, Position.PLAYER2, Position.EMPTY],
         [Position.PLAYER1, Position.FILLED, Position.EMPTY, Position.EMPTY, Position.PLAYER2],
         [Position.EMPTY, Position.FILLED, Position.FILLED, Position.PLAYER2, Position.EMPTY],
         [Position.FILLED, Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.FILLED]
    ]


