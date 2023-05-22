from board import *
import math


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

# minimax with alpha and beta


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
            new_score = minimax_Alpha_Beta(
                b_copy, depth-1, alpha, beta, False)[1]
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
            new_score = minimax_Alpha_Beta(
                b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value
