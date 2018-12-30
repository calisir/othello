from tkinter import *
from tkinter import messagebox

import random

import minimax

class Application:
    def __init__(self):
        # Initialize the windows
        self.window = Tk()
        self.window.title("Othello game")
        self.window.wm_maxsize(width="490", height="540")
        self.window.wm_minsize(width="490", height="540")

        # Initialize
        self.game = False
        self.show_valid_positions = 0  # Shows the valid positions that user can take.
        self.difficulty = 1
        self.mode = 2
        self.color_first_player = 3
        self.heuristic = 4

        self.create_elements()
        self.update_status("Welcome to Othello game!")
        self.window.mainloop()  # Unless user exits shows the window.

    def create_elements(self):
        self.load_images()
        self.create_menu()
        self.create_board()
        self.create_details()

    # Used to display icons.
    def load_images(self):
        self.white_image = PhotoImage(file="white.gif")
        self.black_image = PhotoImage(file="black.gif")
        self.empty_image = PhotoImage(file="empty.gif")
        self.valid_image = PhotoImage(file="valid.gif")

    def create_menu(self):
        self.menu = Menu(self.window)
        self.create_game_menu()
        self.window.config(menu=self.menu)

    def create_game_menu(self):
        gameMenu = Menu(self.menu, tearoff=0)  # The menu will not have a tear-off feature,
        # and choices will be added starting at position 0. i.e. Creates New & Quit in another menu.
        self.menu.add_cascade(label="Game", menu=gameMenu, underline=1)  # To attach the parent menu
        gameMenu.add_command(label="New", command=self.create_game, underline=1)
        gameMenu.add_separator()  # Adds a separator line
        # Checkbox for showing valid positions
        gameMenu.add_checkbutton(label="Show valid positions to play", variable=self.show_valid_positions,
                                     command=self.toggle_show_valid_positions,
                                     underline=0)

        gameMenu.add_separator()  # Adds a separator line
        first_player = Menu(gameMenu, tearoff=0)

        gameMenu.add_cascade(label="Choose First Player", menu=first_player, underline=0)
        first_player.add_radiobutton(label="Black", variable=self.color_first_player,
                                     command=lambda: self.set_first_player("B"),
                                     underline=0)
        first_player.add_radiobutton(label="White", variable=self.color_first_player,
                                     command=lambda: self.set_first_player("W"),
                                     underline=0)

        first_player.invoke(first_player.index("Black")) # Default it is Black

        gameMenu.add_separator()  # Adds a separator line
        mode = Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="Mode", menu=mode, underline=0)
        mode.add_radiobutton(label="Human vs Human", variable=self.mode,
                             command=lambda: self.set_mode(0), underline=0)
        mode.add_radiobutton(label="Human vs Computer", variable=self.mode,
                             command=lambda: self.set_mode(1), underline=1)
        mode.add_radiobutton(label="Computer vs Human", variable=self.mode,
                             command=lambda: self.set_mode(2), underline=12)

        mode.invoke(mode.index("Human vs Computer")) # Default it is choose to Human versus Computer

        gameMenu.add_separator()  # Adds a separator line
        heuristic = Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="Heuristic", menu=heuristic, underline=0)
        heuristic.add_radiobutton(label="Greedy", variable=self.heuristic, underline=0,
                                  command=lambda: self.set_heuristic(minimax.greedy),
                                  value=0)

        heuristic.add_radiobutton(label="Coin-Parity", variable=self.heuristic, underline=0,
                                  command=lambda: self.set_heuristic(minimax.coin_parity),
                                  value=1)

        heuristic.invoke(heuristic.index("Greedy"))  # Default it is chosen as Greedy

        gameMenu.add_separator()  # Adds a separator line
        difficulty = Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="Difficulty", menu=difficulty, underline=0)
        difficulty.add_radiobutton(label="Depth 1",
                                   variable=self.difficulty,
                                   command=lambda: self.set_difficulty(1),
                                   underline=6)
        difficulty.add_radiobutton(label="Depth 2",
                                   variable=self.difficulty,
                                   command=lambda: self.set_difficulty(2),
                                   underline=6)
        difficulty.add_radiobutton(label="Depth 3",
                                   variable=self.difficulty,
                                   command=lambda: self.set_difficulty(3),
                                   underline=6)
        difficulty.add_radiobutton(label="Depth 4",
                                   variable=self.difficulty,
                                   command=lambda: self.set_difficulty(4),
                                   underline=6)

        difficulty.invoke(difficulty.index(1))  # Default it is chosen as 1

        gameMenu.add_separator()  # Adds a separator line
        gameMenu.add_command(label="Quit Game", command=self.quitGame, underline=1)

    def set_mode(self, m):
        self.mode = m
        print('Mode changed to:')
        print(self.mode)

    def set_first_player(self, c):
        self.color_first_player = c
        print('First player changed to:')
        print(self.color_first_player)

    def set_difficulty(self, d):
        self.difficulty = d
        print('Difficulty changed to:')
        print(self.difficulty)

    def set_heuristic(self, h):
        self.heuristic = h
        print('Heuristic changed to:')
        print(self.heuristic)

    def create_board(self):
        self.score = Label(self.window)
        self.score.pack()
        self.board = dict()
        back = Frame(self.window)
        back.pack(fill=BOTH, expand=1)

        for row in range(8):
            frame = Frame(back)
            frame.pack(fill=BOTH, expand=1)
            for column in range(8):
                button = Button(frame,
                                state=DISABLED,
                                command=lambda position=(row, column): self.go(position))
                button["bg"] = "green"
                button.pack(side=LEFT, fill=BOTH, expand=1, padx=0, pady=0)
                self.board.update({(row, column): button})

    def create_details(self):
        self.pass_turn = Button(self.window, text="Pass",
                                state=DISABLED,
                                command=self.pass_turn)
        self.pass_turn.pack(side=RIGHT)
        self.status = Label(self.window)
        self.status.pack(side=LEFT)

    def create_game(self):
        """Instantiate a game from the game module."""
        message = "Are you sure you want to restart?"
        if self.game and \
                not messagebox.askyesno(title="New", message=message):
            return
        if self.mode == 0:
            p1_mode = p2_mode = "H"
        elif self.mode == 1:
            p1_mode = "H"
            p2_mode = "C"
        else:
            p1_mode = "C"
            p2_mode = "H"
        self.game = Game(p1_color=self.color_first_player,
                         p1_mode=p1_mode, p2_mode=p2_mode)
        self.game.start()
        if self.mode == 2:
            self.computer_play()
        message = "Let's play! Now it's the %s's turn." % self.game.turn.color
        self.update_status(message)
        self.update_board()
        self.update_score()
        self.update_pass_turn()

    def toggle_show_valid_positions(self):
        self.show_valid_positions = not self.show_valid_positions
        if self.game:
            self.update_board()

    def pass_turn(self):
        """Pass the turn when it's not possible to play."""
        if not self.game:
            return
        self.game.change_turn()
        if self.game.turn.mode == "C":
            self.computer_play()
        if self.game:
            message = "%s's turn." % self.game.turn.color
            self.update_status(message)
            self.update_board()


    def go(self, position):
        if not self.game:
            return
        if self.game.turn.mode == "C":
            message = "It's the computer turn. Please, wait a moment."
            self.update_status(message=message)
        else:
            self.play(position)

    def play(self, position):
        """Move a piece to the given position."""
        valid = self.game.play(position)
        if not valid:
            message = "Invalid move. It's %s's turn." % self.game.turn.color
            self.update_status(message)
        else:
            message = "%s's turn." % (self.game.turn.color)
            self.update_status(message)
            self.update_board()
            self.update_score()
            self.update_pass_turn()
            self.check_next_turn()

    def computer_play(self):

        minimax.PLAYER = self.game.turn.color
        print('------------------------------')
        print('executing minimax with:')
        print(self.game.board)
        print(self.game.turn.color)
        print('------------------------------')
        position = minimax.minimax(self.game.board,
                                   self.difficulty,
                                   self.game.turn.color,
                                   self.heuristic)[1]
        print('minimax finished with choice: %s' % str(position))
        self.game.play(position)
        message = ("%s's turn." % self.game.turn.color)
        self.update_status(message)
        self.update_board()
        self.update_score()
        self.update_pass_turn()
        self.check_next_turn()

    def check_next_turn(self):
        if self.game.test_end():
            self.update_status("End of game.")
            self.update_board()
            self.update_score()
            self.update_pass_turn()
            self.show_end()
            self.game = False
            return
        if self.game.turn.mode == "C":
            if not has_valid_position(self.game.board, self.game.turn.color):
                self.game.change_turn()
                message = "Computer Passed. Now it's %s's turn." % \
                          (self.game.turn.color)
                self.update_status(message)
                self.update_board()
                self.update_pass_turn()
                return
            else:
                # computer always has a movement to do
                self.update_status("Computer is 'thinking'. Please, wait a moment...")
                self.update_board()
                self.computer_play()

    def show_end(self):
        message = "End of game. %s" % self.game.winning_side()
        messagebox.showinfo(title="End", message=message)

    def update_status(self, message):
        self.status["text"] = message
        self.window.update_idletasks()

    def update_board(self):
        """Update the pieces from the game's board."""
        for row in range(8):
            for column in range(8):
                position = self.board[(row, column)]
                position["state"] = NORMAL
                if self.game.board[(row, column)] == "W":
                    position["image"] = self.white_image
                    position.update_idletasks()
                elif self.game.board[(row, column)] == "B":
                    position["image"] = self.black_image
                    position.update_idletasks()
                else:
                    position["image"] = self.empty_image
                    position.update_idletasks()
        if self.show_valid_positions:
            valid = list(valid_positions(self.game.board, self.game.turn.color))
            for position in valid:
                p = self.board[position]
                p["image"] = self.valid_image
                p.update_idletasks()

    def update_score(self):
        """Update the scores of the players."""
        self.score["text"] = "%s(%s): %s | %s(%s): %s" % \
                             (self.game.player1.color,
                              self.game.player1.mode,
                              self.game.player1.score,
                              self.game.player2.color,
                              self.game.player2.mode,
                              self.game.player2.score)
        self.score.update_idletasks()

    def update_pass_turn(self):
        """Check if it's a pass situation and enable the Pass button."""
        self.pass_turn["state"] = DISABLED
        if not has_valid_position(self.game.board, self.game.turn.color):
            self.pass_turn["state"] = NORMAL
            self.pass_turn.update_idletasks()

    def quitGame(self):
        if messagebox.askyesno(title="Quit", message="Really quit?"):
            quit()


class Game:

    def __init__(self, p1_color="W", p1_mode="H", p2_mode="C"):
        if p1_color == "W":
            p2_color = "B"
        else:
            p2_color = "W"
        self.board = Board()
        self.player1 = Player(color=p1_color, mode=p1_mode)
        self.player2 = Player(color=p2_color, mode=p2_mode)
        self.turn = self.player1

    def start(self):
        self.board[(3, 3)] = self.board[(4, 4)] = "B"
        self.board[(3, 4)] = self.board[(4, 3)] = "W"
        self.update_scores()

    def play(self, position):
        if is_valid_position(self.board, position, self.turn.color):
            move(self.board, position, self.turn.color)
            self.update_scores()
            self.change_turn()
            return True
        else:
            return False

    def update_scores(self):
        self.player1.score = count_pieces(self.board, self.player1.color)
        self.player2.score = count_pieces(self.board, self.player2.color)

    def change_turn(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    def winning_side(self, formatted=True):
        self.update_scores()
        if self.player1.score > self.player2.score:
            winning = self.player1.color
            if not formatted: return winning
        elif self.player1.score < self.player2.score:
            winning = self.player2.color
            if not formatted: return winning
        else:
            if not formatted: return None
            return "Tie."
        if winning == "W":
            return "White win!"
        else:
            return "Black win!"

    def test_end(self):
        return end_game(self.board)

    def __str__(self):
        string = "----------------------\n"
        string += "GAME\n"
        string += "-------\n"
        string += "Turn: %s\n" % self.turn.color
        string += "-------\n"
        string += self.player1.__str__()
        string += "-------\n"
        string += self.player2.__str__()
        string += "-------\n"
        string += "Board:\n"
        string += self.board.__str__()
        string += "----------------------\n"
        return string



class Board(dict):
    def __init__(self):
        for i in range(8):
            for j in range(8):
                self[(i, j)] = "E"

    def __str__(self):
        string = ""
        for i in range(8):
            a = ""
            for j in range(8):
                if self[(i, j)] == "E":
                    a += '-'
                else:
                    a += self[(i, j)]
            string += a + '\n'
        return string


class Player():
    def __init__(self, color, mode):
        self.color = color
        self.mode = mode
        self.score = 0

    def __str__(self):
        string = "Player:\n"
        string += "Color: %s\n" % self.color
        string += "Mode: %s\n" % self.mode
        string += "Score: %s\n" % self.score
        return string


directions = [(1, 0), (0, 1), (-1, 0), (0, -1),
              (1, 1), (1, -1), (-1, 1), (-1, -1)]


def count_pieces(board, color):
    """Count the pieces in the board of the given color."""
    sum = 0
    for i in range(8):
        for j in range(8):
            if board[(i, j)] == color:
                sum += 1
    return sum


def has_valid_position(board, turn):
    """Return if the turn has any valid position."""
    for i in range(8):
        for j in range(8):
            position = (i, j)
            if is_valid_position(board, position, turn):
                return True
    return False


def valid_positions(board, turn):
    """Return a set with all valid positions for the given turn."""
    valid = list()
    for i in range(8):
        for j in range(8):
            position = (i, j)
            if is_valid_position(board, position, turn):
                valid.append(position)

    return set(valid)


def end_game(board):
    """Return a bool.
    Check the end of the game.

    """
    return not has_valid_position(board, "W") and not \
        has_valid_position(board, "B")


def is_valid_position(board, position, turn):
    """Return a bool.
    Check if the given position is valid for this turn.

    """
    if board[position] != "E":
        return False
    for direction in directions:
        between = 0
        i, j = position
        while True:
            try:
                i += direction[0]
                j += direction[1]
                if board[(i, j)] == "E":
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


def move(board, position, turn):
    """Move to the given position a piece of the color of the turn."""

    to_change = []
    for direction in directions:
        between = 0
        i, j = position
        while True:
            try:
                i += direction[0]
                j += direction[1]
                if board[(i, j)] == "E":
                    break
                if board[(i, j)] != turn:
                    between += 1
                elif between > 0:
                    x, y = position
                    for times in range(between + 1):
                        to_change.append((x, y))
                        x += direction[0]
                        y += direction[1]
                    break
                else:
                    break
            except KeyError:
                break
    for item in to_change:
        board[item] = turn

if __name__ == "__main__":
    app = Application()
