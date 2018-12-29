from copy import copy
import random

from util import *
from heuristics import *


PLAYER = "W"
INFINITUM = 100000000000000000000000000000000000000000000


def is_maximizing_player(turn):
    if turn == PLAYER:
        return True
    else:
        return False


def change_turn(turn):
    if turn == "W":
        return "B"
    else:
        return "W"


def minimax(board, depth, turn, heuristic):

    # If depth is 0 or the game has ended
    if depth == 0 or end_game(board):  # Node is a leaf node
        return heuristic(board, PLAYER), None
    else:
        movement = None
        if not has_valid_position(board, turn):
            child = copy(board)
            return minimax(child, depth-1, change_turn(turn), heuristic)[1], movement
        else:
            # if is_maximizing_player(turn):
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
                del child

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
