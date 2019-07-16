import pytest
from blockgame.board import Board
from blockgame.position import Position


@pytest.fixture
def sample_board_medium_move():
    b = Board(5, 5, 3)
    b._board = [[Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.PLAYER2, Position.EMPTY],
                [Position.FILLED, Position.FILLED, Position.EMPTY, Position.FILLED, Position.PLAYER2],
                [Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.FILLED, Position.EMPTY],
                [Position.FILLED, Position.PLAYER1, Position.EMPTY, Position.PLAYER2, Position.FILLED],
                [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED]]
    return b

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


def test_can_move_left():
    board = [[Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.PLAYER1]]
    assert Board.can_move_left(board, 1, 0) == True
    assert Board.can_move_left(board, 3, 0) == False


def test_can_move_right():
    board = [[Position.PLAYER1, Position.FILLED, Position.PLAYER1, Position.EMPTY]]
    assert Board.can_move_right(board, 0, 0) == False
    assert Board.can_move_right(board, 2, 0) == True


def test_can_move_down():
    board = [[Position.PLAYER1, Position.PLAYER1, Position.EMPTY],
             [Position.FILLED, Position.EMPTY, Position.PLAYER1]]
    assert Board.can_move_down(board, 0, 0) == False
    assert Board.can_move_down(board, 1, 0) == True
    assert Board.can_move_down(board, 2, 1) == False


def test_apply_gravity():
    b = Board(9, 3, 2)
    b._board = [
        [Position.PLAYER1, Position.PLAYER2, Position.PLAYER1, Position.PLAYER2, Position.PLAYER1, Position.PLAYER2,
         Position.FILLED, Position.FILLED, Position.FILLED],
        [Position.EMPTY, Position.EMPTY, Position.EMPTY, Position.EMPTY, Position.FILLED, Position.FILLED,
         Position.FILLED, Position.FILLED, Position.FILLED],
        [Position.EMPTY, Position.EMPTY, Position.FILLED, Position.FILLED, Position.FILLED, Position.FILLED,
         Position.PLAYER1, Position.PLAYER2, Position.FILLED]]
    b._apply_gravity()
    assert b._board == [
        [Position.EMPTY, Position.EMPTY, Position.EMPTY, Position.EMPTY, Position.PLAYER1, Position.PLAYER2,
         Position.FILLED, Position.FILLED, Position.FILLED],
        [Position.EMPTY, Position.EMPTY, Position.PLAYER1, Position.PLAYER2, Position.FILLED, Position.FILLED,
         Position.FILLED, Position.FILLED, Position.FILLED],
        [Position.PLAYER1, Position.PLAYER2, Position.FILLED, Position.FILLED, Position.FILLED, Position.FILLED,
         Position.PLAYER1, Position.PLAYER2, Position.FILLED]]


def test_no_moves_left():
    player1 = Position.PLAYER1
    player2 = Position.PLAYER2
    board = [[Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED]]
    assert Board.no_moves_left(board, player1) == True
    assert Board.no_moves_left(board, player2) == True

    board = [[Position.FILLED, Position.EMPTY, Position.FILLED, Position.PLAYER1]]
    assert Board.no_moves_left(board, player1) == True
    assert Board.no_moves_left(board, player2) == True

    board = [[Position.PLAYER1, Position.EMPTY, Position.FILLED, Position.PLAYER2]]
    assert Board.no_moves_left(board, player1) == False
    assert Board.no_moves_left(board, player2) == True

    board = [[Position.PLAYER1, Position.PLAYER2, Position.FILLED, Position.FILLED]]
    assert Board.no_moves_left(board, player1) == True
    assert Board.no_moves_left(board, player2) == True

    board = [[Position.EMPTY, Position.PLAYER2, Position.PLAYER1, Position.FILLED]]
    assert Board.no_moves_left(board, player1) == True
    assert Board.no_moves_left(board, player2) == False

    board = [[Position.PLAYER2, Position.FILLED, Position.FILLED, Position.PLAYER1]]
    assert Board.no_moves_left(board, player1) == True
    assert Board.no_moves_left(board, player2) == True


@pytest.mark.usefixtures("sample_board_medium")
def test_move_player(sample_board_medium):
    sample_board_medium._move_player(Position.PLAYER1)
    sample_board_medium.print()
