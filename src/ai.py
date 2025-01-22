import math
from board import Board
from move import Move
from copy import deepcopy
from const import *
from piece import *

# A simple evaluation function for the AI
def evaluate_board(board, color):
    score = 0
    opponent_color = get_opponent_color(color)
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.squares[row][col].piece
            if piece:
                if piece.color == color:
                    score += piece.value
                else:
                    score -= piece.value
    return score



def alpha_beta(board, depth, alpha, beta, maximizing_player, color):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, color), None

    legal_moves = board.get_all_valid_moves(color if maximizing_player else get_opponent_color(color))

    if not legal_moves:
        # No legal moves available
        return evaluate_board(board, color), None

    best_move = None

    if maximizing_player:
        max_eval = -math.inf
        for move in legal_moves:
            board_copy = board.copy()
            board_copy.move(move.piece, move)
            eval, _ = alpha_beta(board_copy, depth - 1, alpha, beta, False, color)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = math.inf
        for move in legal_moves:
            board_copy = board.copy()
            board_copy.move(move.piece, move)
            eval, _ = alpha_beta(board_copy, depth - 1, alpha, beta, True, color)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_opponent_color(color):
    return 'white' if color == 'black' else 'black'
