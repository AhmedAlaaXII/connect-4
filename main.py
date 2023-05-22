from board import *
import matplotlib.pyplot as plt
import pygame
import sys
import math
from AI_algorithms import *

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

x = input("wiht alpha-beta or not (y,n)")
y = input(
    "enter the level of player 1 (beginner , intermediate or advanced )")
z = input(
    "enter the level of player 2 (beginner , intermediate or advanced )")
# function to create a board


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
        pygame.time.wait(500)
        if x == 'n':
            if y == "beginner":
                col, minimax_score = minimax(board, 2, True)
            if y == "intermediate":
                col, minimax_score = minimax(board, 3, True)
            if y == "advanced":
                col, minimax_score = minimax(board, 4, True)
        elif x == 'y':
            if y == "beginner":
                col, minimax_score = minimax_Alpha_Beta(
                    board, 3, -math.inf, math.inf, True)
            if y == "intermediate":
                col, minimax_score = minimax_Alpha_Beta(
                    board, 4, -math.inf, math.inf, True)
            if y == "advanced":
                col, minimax_score = minimax_Alpha_Beta(
                    board, 5, -math.inf, math.inf, True)
        else:
            print("Enter the type of algorithm")
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
            pygame.display.update()
            # Waiting time in milliseconds (0.5 seconds)

    # Ask for player 2  input
    if turn == AI and not game_over:
        pygame.time.wait(500)
        if x == 'n':
            if y == "beginner":
                col, minimax_score = minimax(board, 2, True)
            if y == "intermediate":
                col, minimax_score = minimax(board, 3, True)
            if y == "advanced":
                col, minimax_score = minimax(board, 4, True)
        elif x == 'y':
            if y == "beginner":
                col, minimax_score = minimax_Alpha_Beta(
                    board, 3, -math.inf, math.inf, True)
            if y == "intermediate":
                col, minimax_score = minimax_Alpha_Beta(
                    board, 4, -math.inf, math.inf, True)
            if y == "advanced":
                col, minimax_score = minimax_Alpha_Beta(
                    board, 5, -math.inf, math.inf, True)
        else:
            print("Enter the type of algorithm")

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = myfont.render("PLAYER 2 WINS!!!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
                print_board(board)
                draw_board(board)
                pygame.display.update()
            turn += 1
            turn = turn % 2
    if game_over:
        pygame.time.wait(3000)

measure_performance()
