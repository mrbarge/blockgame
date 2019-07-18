import pytest
from blockgame.board import Board
from blockgame.position import Position


@pytest.fixture
def sample_board_small_score():
    b = Board(3, 5, 3)
    b._board = [[Position.PLAYER1, Position.EMPTY, Position.EMPTY],
                [Position.FILLED, Position.FILLED, Position.FILLED],
                [Position.PLAYER1, Position.EMPTY, Position.EMPTY],
                [Position.FILLED, Position.EMPTY, Position.EMPTY],
                [Position.FILLED, Position.FILLED, Position.FILLED]]
    return b


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


@pytest.mark.usefixtures("sample_board_medium_move")
def test_move_player1(sample_board_medium_move):
    sample_board_medium_move._move_player(2, Position.PLAYER1)
    assert sample_board_medium_move._board == [
        [Position.EMPTY, Position.EMPTY, Position.EMPTY, Position.PLAYER2, Position.EMPTY],
        [Position.FILLED, Position.FILLED, Position.EMPTY, Position.FILLED, Position.EMPTY],
        [Position.EMPTY, Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.PLAYER2],
        [Position.FILLED, Position.PLAYER1, Position.PLAYER1, Position.PLAYER2, Position.FILLED],
        [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED]
    ]


@pytest.mark.usefixtures("sample_board_medium_move")
def test_move_player2(sample_board_medium_move):
    sample_board_medium_move._move_player(2, Position.PLAYER2)
    assert sample_board_medium_move._board == [
        [Position.PLAYER1, Position.EMPTY, Position.EMPTY, Position.EMPTY, Position.EMPTY],
        [Position.FILLED, Position.FILLED, Position.EMPTY, Position.FILLED, Position.EMPTY],
        [Position.PLAYER1, Position.PLAYER2, Position.EMPTY, Position.FILLED, Position.PLAYER2],
        [Position.FILLED, Position.PLAYER1, Position.PLAYER2, Position.EMPTY, Position.FILLED],
        [Position.EMPTY, Position.PLAYER1, Position.FILLED, Position.FILLED, Position.FILLED]
    ]


@pytest.mark.usefixtures("sample_board_small_score")
def test_move_player1_score(sample_board_small_score):
    p1, p2 = sample_board_small_score._move_player(2, Position.PLAYER1)
    assert sample_board_small_score._board == [
        [Position.EMPTY, Position.EMPTY, Position.EMPTY],
        [Position.FILLED, Position.FILLED, Position.FILLED],
        [Position.EMPTY, Position.EMPTY, Position.EMPTY],
        [Position.FILLED, Position.EMPTY, Position.EMPTY],
        [Position.FILLED, Position.FILLED, Position.FILLED]
    ]
    assert p1 == 2
    assert p2 == 0


@pytest.mark.usefixtures("sample_board_medium")
def test_player_columns(sample_board_medium):
    assert sample_board_medium.player_columns(Position.PLAYER1) == [0, 1]
    assert sample_board_medium.player_columns(Position.PLAYER2) == [3, 4]