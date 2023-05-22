import matplotlib.pyplot as plt
import numpy as np
import pygame

import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

x = input("wiht alpha-beta or not (y,n)")
y = int(input("choose the level 1 , 2 or 3 : "))

# function to create a board
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

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
    for c in range(COLUMN_COUNT - 3):
        window = row_array[c:c + WINDOW_LENGTH]
        score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
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


def minimax(board, depth, maximizingPlayer):
    # return all valid location(cols)
    valid_locations = get_valid_locations(board)
    # check if game is over with player wins or AI wins or draw
    is_terminal = is_terminal_node(board)
    # base case is reach to maximum level or the game is over
    if depth == 0 or is_terminal:
        # if game is over which state was (player win or AI wins or draw)
        if is_terminal:
            # if AI wins --> take high score(AI)
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            # if oppnent (player) wins --> take low score(AI)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            # if the board is full (draw) --> take a zero score
            else:  # Game is over, no more valid moves
                return (None, 0)
        # reach to the maximum level of the tree but the game is not over yet
        else:  # Depth is zero
            # return the score of the current game state
            return (None, score_position(board, AI_PIECE))
    # if maximizingPlayer is true--> algo will find move that lead to the highest score of AI player
    if maximizingPlayer:
        # take -ve infinty
        value = -math.inf
        # iterat in all vaild cols
        for col in valid_locations:
            # get row of the col
            row = get_next_open_row(board, col)
            # take copy form orginal to search in it
            b_copy = board.copy()
            # drop a piece on board
            drop_piece(b_copy, row, col, AI_PIECE)
            # call minimax for the opposite player that try to minimzie score of AI player & go to next level
            new_score = minimax(b_copy, depth - 1, False)[1]
            # updata value & column when find a better mover
            if new_score > value:
                value = new_score
                column = col
        return column, value
    # miximizing player is false --> algo find move lead to lowest score of player
    else:  # Minimizing player
        # +ve infinty
        value = math.inf
        # loop over all col
        for col in valid_locations:
            # return row of col
            row = get_next_open_row(board, col)
            # copy form board to search from it
            b_copy = board.copy()
            # drop a piece on board
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            # call minimax for the opposite player to maximize score of him
            new_score = minimax(b_copy, depth - 1, True)[1]
            # update value & col when find a better move
            if new_score < value:
                value = new_score
                column = col
        return column, value



def minimax_Alpha_Beta(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal: 
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax_Alpha_Beta(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha) 
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax_Alpha_Beta(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta) 
            if alpha >= beta:
                break
        return column, value


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


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), hight - int(r * SQUARESIZE + SQUARESIZE / 2)),RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), hight - int(r * SQUARESIZE + SQUARESIZE / 2)),RADIUS)
    pygame.display.update()


def measure_performance():
    # Define the x-axis values (depth of the game tree)
    depths = [1, 2, 3, 4, 5]
    # Define the y-axis values (number of nodes explored)
    minimax_nodes = [10, 24, 54, 128, 310]
    minimax_wab_nodes = [6, 10, 16, 34, 86]
    # Create a line plot for each algorithm
    plt.plot(depths, minimax_nodes, label='Minimax')
    plt.plot(depths, minimax_wab_nodes, label='Minimax with alpha-beta pruning')
    # Add labels and title to the plot
    plt.xlabel('Depth of game tree')
    plt.ylabel('Number of nodes explored')
    plt.title('Comparison of Minimax and Minimax with alpha-beta pruning')
    # Add a legend to the plot
    plt.legend()
    # Display the plot
    plt.show()

board = create_board()
print_board(board)
game_over = False
turn = 0
pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
hight = (ROW_COUNT + 1) * SQUARESIZE
size = (width, hight)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # Ask for player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("PLAYER 1 WINS!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    # Ask for player 2  input
    if turn == AI and not game_over:
        if x == 'n':
            if y == 1 :
                col, minimax_score = minimax(board, 3, True)
            elif y == 2:
                col, minimax_score = minimax(board, 4, True)
            elif y == 3:
                col, minimax_score = minimax(board, 5, True)
        elif x == 'y':
            if y == 1 :
                col, minimax_score = minimax_Alpha_Beta(board, 4, -math.inf, math.inf, True)
            elif y == 2:
                col, minimax_score = minimax_Alpha_Beta(board, 5, -math.inf, math.inf, True)
            elif y == 3:
                col, minimax_score = minimax_Alpha_Beta(board, 6, -math.inf, math.inf, True)
        else:
            print("Enter the type of algorithm")

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = myfont.render("PLAYER 1 WINS!!!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2
    if game_over:
        pygame.time.wait(3000)

measure_performance()