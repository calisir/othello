from othello import directions


def count_pieces(board, color):
    count = 0
    for i in range(8):
        for j in range(8):
            if board[(i, j)] == color:
                count += 1
    return count


def has_valid_position(board, turn):
    for i in range(8):
        for j in range(8):
            position = (i, j)
            if is_valid_position(board, position, turn):
                return True
    return False


def valid_positions(board, turn):
    valid = list()
    for i in range(8):
        for j in range(8):
            position = (i, j)
            if is_valid_position(board, position, turn):
                valid.append(position)

    return set(valid)


def end_game(board):
    return not has_valid_position(board, "W") and not \
        has_valid_position(board, "B")


def is_valid_position(board, position, turn):
    if board[position] != "EMPTY":
        return False
    for direction in directions:
        between = 0
        i, j = position
        while True:
            try:
                i += direction[0]
                j += direction[1]
                if board[(i, j)] == "EMPTY":
                    break
                if board[(i, j)] != turn:
                    between += 1
                elif between > 0:
                    return True
                else:
                    break
            except KeyError:
                break
    return False