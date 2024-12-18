"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn  = sum(True for row in board for i in row if i is not EMPTY)

    return X if turn%2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return [(i,j) for i, row in enumerate(board) for j, col in enumerate(row) if col == EMPTY]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not a valid move")

    new_board = deepcopy(board)
    row, col = action
    new_board[row][col] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    line = [
        # Horizontal rows
        {(0, 0), (0, 1), (0, 2)},
        {(1, 0), (1, 1), (1, 2)},
        {(2, 0), (2, 1), (2, 2)},

        # Vertical columns
        {(0, 0), (1, 0), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 2), (1, 2), (2, 2)},

        # Diagonals
        {(0, 0), (1, 1), (2, 2)},
        {(0, 2), (1, 1), (2, 0)},
    ]

    values = [{board[i][j] for i, j in row} for row in line]

    winner = [i for i in values if len(i)==1 and i != {EMPTY}]

    return [i for i in winner[0]][0] if winner else None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(j!=EMPTY for i in board for j in i)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 2*int(winner(board)==X)-1 if winner(board) is not None else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def minimax_helper(board, alpha = -math.inf, beta = math.inf):
        current_player = player(board)

        #if the game ends
        if terminal(board):
            return None, utility(board)

        #Maximixing player
        elif current_player == X:
            best_max = -math.inf
            best_actions = None
            for action in actions(board):
                new_max = minimax_helper(result(board, action), alpha=alpha, beta=beta)[1]
                if new_max > best_max:
                    best_max = new_max
                    best_actions = action
                alpha = max(alpha, new_max)
                if alpha >= beta:
                    break
            return best_actions, best_max

        #minimizing player
        elif current_player == O:
            best_min = math.inf
            best_actions = None
            for action in actions(board):
                new_min = minimax_helper(result(board, action), alpha=alpha, beta=beta)[1]
                if new_min < best_min:
                    best_min = new_min
                    best_actions = action
                beta = min(beta, new_min)
                if alpha >= beta:
                    break
            return best_actions, best_min

    return minimax_helper(board)[0]