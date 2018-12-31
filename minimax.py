from copy import copy
from othello import *


PLAYER = "B"
INF = 9999999999999999


def change_turn(turn):
    if turn == "W":
        return "B"
    else:
        return "W"


def node_c():
    return node_count

# Minimax algorithms with Alpha-Beta pruning


def greedy_alpha_beta_minimax(board, depth, turn, alpha, beta):
    global node_count
    #print("Depth: "+str(depth))
    movement = None
    if depth == 0 or end_game(board):
        return greedy(board, PLAYER), None
    else:
        valid = valid_positions(board, turn)
        ties = []

        # if maximizing player
        if turn == PLAYER:
            best_value = -INF
            for position in valid:
                child_node = copy(board)
                move(child_node, position, turn)
                print("Depth in Situation 2: " + str(depth))
                child_value = greedy_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                del child_node

                best_value = max(best_value, child_value)
                alpha = max(alpha, best_value)
                ties.append((alpha, position))
                node_count += 1

                if beta <= alpha:
                    break

            best_value, movement = random.choice(ties)
            return best_value, movement

        else:
            best_value = INF
            for position in valid:
                child_node = copy(board)
                move(child_node, position, turn)
                print("Depth in Situation 2: " + str(depth))
                child_value = greedy_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                del child_node

                best_value = min(best_value, child_value)
                beta = min(beta, best_value)
                ties.append((beta, position))
                node_count += 1

                if beta <= alpha:
                    break

            best_value, movement = random.choice(ties)
            return best_value, movement


def coinparity_alpha_beta_minimax(board, depth, turn, alpha, beta):
    global node_count

    #print("Depth: "+str(depth))
    movement = None
    if depth == 0 or end_game(board):
        return coin_parity(board, PLAYER), None
    else:
        valid = valid_positions(board, turn)
        ties = []

        # if maximizing player
        if turn == PLAYER:
            best_value = -INF
            for position in valid:
                child_node = copy(board)
                move(child_node, position, turn)
                # print("Depth in Situation 2: " + str(depth))
                child_value = coinparity_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                del child_node

                best_value = max(best_value, child_value)
                alpha = max(alpha, best_value)
                ties.append((alpha, position))
                node_count += 1

                if beta <= alpha:
                    break

            best_value, movement = random.choice(ties)
            return best_value, movement

        else:
            best_value = INF
            for position in valid:
                child_node = copy(board)
                move(child_node, position, turn)
                # print("Depth in Situation 2: " + str(depth))
                child_value = coinparity_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                del child_node

                best_value = min(best_value, child_value)
                beta = min(beta, best_value)
                ties.append((beta, position))
                node_count += 1

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