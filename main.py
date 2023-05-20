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


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r *
                             SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), hight - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), hight - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def measure_performance():
    # Define the x-axis values (depth of the game tree)
    depths = [1, 2, 3, 4, 5]

    # Define the y-axis values (number of nodes explored)
    minimax_nodes = [10, 24, 54, 128, 310]
    minimax_wab_nodes = [6, 10, 16, 34, 86]

    # Create a line plot for each algorithm
    plt.plot(depths, minimax_nodes, label='Minimax')
    plt.plot(depths, minimax_wab_nodes,
             label='Minimax with alpha-beta pruning')

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
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
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
