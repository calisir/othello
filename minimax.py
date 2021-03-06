from copy import copy

import driver
from othello import *


PLAYER = "W"
INF = 9999999999999999
node_count = 0


def change_turn(turn):
    if turn == "W":
        return "B"
    else:
        return "W"


def node_c():
    return node_count


def reset_node_count():
    global node_count
    node_count=0

# Minimax algorithms with Alpha-Beta pruning


def greedy_alpha_beta_minimax(board, depth, turn, alpha, beta):
    #print("Depth: "+str(depth))

    global node_count  # To change variable as global
    movement = None

    # If the depth is 0 or game has reached an end.
    if depth == 0 or driver.end_game(board):
        return greedy(board, PLAYER), movement
    else:
        valid = driver.valid_positions(board, turn)  # Set of valid positions to play
        ties = []  # List of ties that may arise

        if not driver.has_valid_position(board, turn):
            child_node = copy(board)
            return greedy_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0], movement
        else:
            # if maximizing player
            if turn == PLAYER:
                best_value = -INF
                for position in valid:  # For every valid position tuple
                    child_node = copy(board)  # Not to use the original board we create a dummy one
                    move(child_node, position, turn)  # Hypothetically move it
                    print("MAX-Depth in Situation 2: " + str(depth))
                    child_value = greedy_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                    print("MAX-Child value: "+str(child_value))
                    del child_node  # Then delete it

                    # best
                    best_value = max(best_value, alpha)
                    #print("x: "+str(x))

                    #alpha
                    alpha = max(alpha, best_value)  # Best value that maximizer can currently guarantee
                    #print("alpha: "+str(alpha))
                    node_count += 1  # Increase node count by 1 to know that we have visited this node before pruning

                    if beta <= alpha:  # Alpha-Beta pruning
                        break

                    if best_value == child_value:
                        print("1-Best Value: " + str(best_value))
                        print("1-Position Value: " + str(position))
                        ties.append((best_value, position))  # Append the value to the ties list
                    elif child_value > best_value:
                        best_value = child_value
                        print("2-Best Value: " + str(best_value))
                        print("2-Position Value: " + str(position))
                        ties = [(best_value, position)]  # Get that best value and its position


                best_value, movement = random.choice(ties)
                return best_value, movement

            # if minizing player
            else:
                best_value = INF
                for position in valid:  # For every valid position tuple
                    child_node = copy(board)  # Not to use the original board we create a dummy one
                    move(child_node, position, turn)  # Hypothetically move it
                    print("MIN-Depth in Situation 2: " + str(depth))
                    child_value = greedy_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                    print("MIN-Child value: " + str(child_value))
                    del child_node

                    # best
                    best_value = min(best_value, child_value)
                    #print("y: "+str(y))
                    node_count += 1

                    # beta
                    beta = min(beta, best_value)  # Best value that minimizer can currently guarantee

                    if beta <= alpha:  # Alpha-Beta pruning
                        break

                    if best_value == child_value:
                        print("3-Best Value: " + str(best_value))
                        print("3-Position Value: " + str(position))
                        ties.append((best_value, position))  # Append the value to the ties list
                    elif child_value < best_value:
                        best_value = child_value
                        print("4-Best Value: " + str(best_value))
                        print("4-Position Value: " + str(position))
                        ties = [(best_value, position)]  # Get that best value and its position

                best_value, movement = random.choice(ties)
                return best_value, movement


def coinparity_alpha_beta_minimax(board, depth, turn, alpha, beta):
    global node_count
    # print("Depth: "+str(depth))

    movement = None

    # If the depth is 0 or game has reached an end.
    if depth == 0 or driver.end_game(board):
        return coin_parity(board, PLAYER), movement
    else:
        valid = driver.valid_positions(board, turn)  # Set of valid positions to play
        ties = []

        if not driver.has_valid_position(board, turn):
            child_node = copy(board)
            return coinparity_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0], movement
        else:
            # if maximizing player
            if turn == PLAYER:
                best_value = -INF
                for position in valid:  # For every valid position tuple
                    child_node = copy(board)  # Not to use the original board we create a dummy one
                    move(child_node, position, turn)  # Hypothetically move it
                    print("MAX-Depth in Situation 2: " + str(depth))
                    child_value = coinparity_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                    print("MAX-Child value: " + str(child_value))
                    del child_node

                    # best
                    best_value = max(best_value, alpha)  # Best value that maximizer can currently guarantee
                    # print("x: "+str(x))

                    # alpha
                    alpha = max(alpha, best_value)
                    # print("alpha: "+str(alpha))
                    node_count += 1

                    if beta <= alpha:
                        break

                    if best_value == child_value:
                        print("1-Best Value: " + str(best_value))
                        print("1-Position Value: " + str(position))
                        ties.append((best_value, position))
                    elif child_value > best_value:
                        best_value = child_value
                        print("2-Best Value: " + str(best_value))
                        print("2-Position Value: " + str(position))
                        ties = [(best_value, position)]

                best_value, movement = random.choice(ties)
                return best_value, movement

            else:
                best_value = INF
                for position in valid:
                    child_node = copy(board)
                    move(child_node, position, turn)
                    print("MIN-Depth in Situation 2: " + str(depth))
                    child_value = coinparity_alpha_beta_minimax(child_node, depth - 1, change_turn(turn), alpha, beta)[0]
                    print("MIN-Child value: " + str(child_value))
                    del child_node

                    # best
                    best_value = min(best_value, child_value)  # Best value that minimizer can currently guarantee
                    # print("y: "+str(y))

                    # beta
                    beta = min(beta, best_value)
                    node_count += 1

                    if beta <= alpha:
                        break

                    if best_value == child_value:
                        print("3-Best Value: " + str(best_value))
                        print("3-Position Value: " + str(position))
                        ties.append((best_value, position))
                    elif child_value < best_value:
                        best_value = child_value
                        print("4-Best Value: " + str(best_value))
                        print("4-Position Value: " + str(position))
                        ties = [(best_value, position)]

                best_value, movement = random.choice(ties)
                return best_value, movement


# Heuristics


def greedy(board, turn):
    if turn == "W":
        print("GREEDY-W-COUNT " + str(driver.count_pieces(board, "W")))
        return driver.count_pieces(board, "W")
    else:
        print("GREEDY-B-COUNT " + str(driver.count_pieces(board, "B")))
        return driver.count_pieces(board, "B")


def coin_parity(board, turn):
    if turn == PLAYER:
        max_player = "W"
        min_player = "B"
    else:
        max_player = "B"
        min_player = "W"

    print("1: " + str(driver.count_pieces(board, max_player)))
    print("2: " + str(driver.count_pieces(board, min_player)))

    result = 100 * (driver.count_pieces(board, max_player) - driver.count_pieces(board, min_player)) / (
            driver.count_pieces(board, max_player) + driver.count_pieces(board, min_player))
    print("COIN-PARITY: "+str(result))
    return result