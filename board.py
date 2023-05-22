import numpy as np
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# function flip board to make inputs start from down to top


def print_board(board):
    print(np.flip(board, 0))


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# functino to check of column is empty fo fill or not


def is_valid_location(board, col):
    return board[5][col] == 0

# function to set piece 1,2 to specific location


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def winning_move(board, piece):
    # check horizontal location for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                return True
    # check vertical location for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                return True
    # check +ve diagonal location for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                    c + 3] == piece:
                return True
    # check -ve diagonal location for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                    c + 3] == piece:
                return True
# function to evaluate the strenght of window(4 consecutive pieces) whatever vertical or horizontal or diagonal
# and in terms of state add score


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    # check if piece relate to the opponent player
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    # if window has 4 piece has the same color add 100 indicate very strong position for AI player
    if window.count(piece) == 4:
        score += 100
    # if widow has 3 piece has the same color add 5 indicate moderate strong posision for AI player
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    # if window has 2 piece has the same color add 2 indicate to relatively weak posision for AI player
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    # if window has 3 piece has the same color for opponent player indicate that the opponent has a strong position
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score


# function is used to evaluate the strength of the entire Connect Four board for a specific player
def score_position(board, piece):
    score = 0
    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
    for c in range(COLUMN_COUNT - 3):
        window = row_array[c:c + WINDOW_LENGTH]
        score += evaluate_window(window, piece)
    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# function to get all vaild location


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# function returns the column that leads to the strongest board position for the given player


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col
