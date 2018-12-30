from copy import copy
from othello import *


PLAYER = "W"
INFINITUM = 100000000000000000000000000000000000000000000


def change_turn(turn):
    if turn == "W":
        return "B"
    else:
        return "W"
"""
def minimax(board, depth, turn, heuristic):
    if depth == 0 or end_game(board):
        return heuristic(board, PLAYER), None
    else:
        movement = None
        if not has_valid_position(board, turn):
            child = copy(board)
            return minimax(child, depth-1, change_turn(turn), heuristic)[0], movement
        else:
            if turn == PLAYER:
                best = -INFINITUM
            else:
                best = INFINITUM
            valid = valid_positions(board, turn)
            ties = []
            for position in valid:
                child = copy(board)
                move(child, position, turn)
                child_value = minimax(child, depth-1, change_turn(turn), heuristic)[0]
                del(child)

                if turn == PLAYER:
                    if best == child_value:
                        ties.append((best, position))
                    elif child_value > best:
                        best = child_value
                        ties = [(best, position)]
                else:
                    if best == child_value:
                        ties.append((best, position))
                    elif child_value < best:
                        best = child_value
                        ties = [(best, position)]
            best, movement = random.choice(ties)
            return best, movement
"""

#  def alpha_beta_greedy(board, depth, turn, alpha, beta):




def minimax(board, depth, turn, alpha, beta):
    #print("Depth: "+str(depth))
    movement = None
    if depth == 0 or end_game(board):
        return greedy(board, PLAYER), None
    else:
        valid = valid_positions(board, turn)
        ties = []

        # if maximizing player
        if turn == PLAYER:
            best_value = -INFINITUM
            for position in valid:
                child_node = copy(board)
                move(child_node, position, turn)
                print("Depth in Situation 2: " + str(depth))
                child_value = minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                del child_node

                best_value = max(best_value, child_value)
                alpha = max(alpha, best_value)
                ties.append((alpha, position))

                if beta <= alpha:
                    break

            best_value, movement = random.choice(ties)
            return best_value, movement

        else:
            best_value = INFINITUM
            for position in valid:
                child_node = copy(board)
                move(child_node, position, turn)
                print("Depth in Situation 2: " + str(depth))
                child_value = minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                del child_node

                best_value = min(best_value, child_value)
                beta = min(beta, best_value)
                ties.append((beta, position))

                if beta <= alpha:
                    break

            best_value, movement = random.choice(ties)
            return best_value, movement


# Heuristics


def greedy(board, turn):
    if turn == "W":
        return count_pieces(board, "W")
    else:
        return count_pieces(board, "B")


def coin_parity(board, turn):
    if turn == PLAYER:
        max_player = "W"
        min_player = "M"
    else:
        max_player = "B"
        min_player = "W"

    return 100 * (count_pieces(board, max_player) - count_pieces(board, min_player)) / (count_pieces(board, max_player) + count_pieces(board, min_player))