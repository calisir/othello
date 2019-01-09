from tkinter import *
from tkinter import messagebox

import random

import minimax
import driver

MAX = 9999
MIN = -9999

directions = [(1, 0), (0, 1), (-1, 0), (0, -1),
              (1, 1), (1, -1), (-1, 1), (-1, -1)]


class Othello:
    def __init__(self):
        # Initialize the windows
        self.window = Tk()
        self.window.title("Othello")
        self.window.wm_maxsize(width="490", height="600")
        self.window.wm_minsize(width="490", height="600")

        # Initialize
        self.game = False
        self.show_valid_positions = 0  # Shows the valid positions that user can take.
        self.depth = 1
        self.playing_against = 2
        self.color_first_player = "B"  # Always Black starts first
        self.heuristic = 2

        self.white_image = PhotoImage(file="white.gif")
        self.black_image = PhotoImage(file="black.gif")
        self.empty_image = PhotoImage(file="empty.gif")
        self.valid_image = PhotoImage(file="valid.gif")

        self.menu = Menu(self.window)
        self.create_game_menu()
        self.window.config(menu=self.menu)


        self.create_board()

        self.pass_turn = Button(self.window, text="Pass",
                                state=DISABLED,
                                command=self.pass_turn)
        self.pass_turn.pack(side=RIGHT)
        self.status = Label(self.window)
        self.status.pack(side=LEFT)

        self.update_status("Welcome to the Othello game!")
        self.window.mainloop()  # Unless user exits shows the window.

        #master.bind("N", self.create_game)

    def create_game_menu(self):
        gameMenu = Menu(self.menu, tearoff=0)  # The menu will not have a tear-off feature,
        # and choices will be added starting at position 0. i.e. Creates New & Quit in another menu.
        self.menu.add_cascade(label="Game", menu=gameMenu, underline=1)  # To attach the parent menu
        gameMenu.add_command(label="New Game", command=self.create_game, underline=1, accelerator="N")

        gameMenu.add_separator()  # Adds a separator line
        # Checkbox for showing valid positions
        gameMenu.add_checkbutton(label="Show valid positions to play", variable=self.show_valid_positions,
                                     command=self.toggle_show_valid_positions,
                                     underline=0)

        gameMenu.add_separator()  # Adds a separator line
        playing_against = Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="Playing Against", menu=playing_against, underline=0)
        playing_against.add_radiobutton(label="Human vs Human", variable=self.playing_against,
                             command=lambda: self.set_playing_against(0), underline=0)
        playing_against.add_radiobutton(label="Human vs Computer", variable=self.playing_against,
                             command=lambda: self.set_playing_against(1), underline=1)
        playing_against.add_radiobutton(label="Computer vs Computer", variable=self.playing_against,
                             command=lambda: self.set_playing_against(2), underline=12)

        playing_against.invoke(playing_against.index("Human vs Computer"))
        # Default it is choose to Human versus Computer

        gameMenu.add_separator()  # Adds a separator line
        heuristic = Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="Heuristic", menu=heuristic, underline=0)
        heuristic.add_radiobutton(label="Greedy", variable=self.heuristic, underline=0,
                                  command=lambda: self.set_heuristic(0),
                                  value=0)

        heuristic.add_radiobutton(label="Coin-Parity", variable=self.heuristic, underline=0,
                                  command=lambda: self.set_heuristic(1),
                                  value=1)

        heuristic.invoke(heuristic.index("Greedy"))  # Default it is chosen as Greedy

        gameMenu.add_separator()  # Adds a separator line
        gameMenu.add_command(label="Quit Game", command=self.quit_game, underline=1)

    def set_playing_against(self, m):
        self.playing_against = m
        print('Playings against is set to:')
        if self.playing_against == 0:
            print("Human vs Human")
        elif self.playing_against == 1:
            print("Computer vs Human")
        else:
            print("Computer vs Computer")

        # Set Visited Nodes to 0 for every new game
        global node_count
        node_count = 0

    def set_heuristic(self, h):
        #print("h: "+str(h))
        self.heuristic = h
        print('Heuristic set to:')
        if self.heuristic == 0:
            print("Greedy")
        elif self.heuristic == 1:
            print("Coin Parity")

        # Set Visited Nodes to 0 for every new game
        global node_count
        node_count = 0

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

    def create_game(self):

        minimax.reset_node_count()

        if minimax.node_c() == 0:
            message = "Node count is resetted."
            messagebox.showinfo(title="Node Count Reset", message=message)

        message = "Are you sure you want to restart?"
        if self.game and \
                not messagebox.askyesno(title="New", message=message):
            return

        # According to the settings decide the roles of each player.
        if self.playing_against == 0:
            p1_playing_against = p2_playing_against = "HUMAN"
        elif self.playing_against == 1:
            p1_playing_against = "HUMAN"
            p2_playing_against = "COMPUTER"
        else:
            p1_playing_against = "COMPUTER"
            p2_playing_against = "COMPUTER"


        self.game = Game(p1_color=self.color_first_player,
                         p1_playing_against=p1_playing_against, p2_playing_against=p2_playing_against)
        self.game.start()

        # If playing against computer
        if self.playing_against == 2:
            self.computer_play()
        #print("xxx   " + self.game.turn.color)
        #message = "It's" + self.game.turn.color+"'s turn."
        self.update_status(message)
        self.update_board()
        self.update_score()
        self.update_pass_turn()

    def toggle_show_valid_positions(self):
        self.show_valid_positions = not self.show_valid_positions
        if self.game:
            self.update_board()

    def pass_turn(self):
        if not self.game:
            return
        self.game.change_turn()
        if self.game.turn.playing_against == "COMPUTER":
            self.computer_play()
        if self.game:
            message = "%s's turn." % self.game.turn.color
            self.update_status(message)
            self.update_board()

    def go(self, position):
        if not self.game:
            #print("XXXXXXX")
            self.update_pass_turn()
            return
        if self.game.turn.playing_against == "COMPUTER":
            message = "It's the computer turn."
            self.update_status(message=message)
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            self.play(position)
        else:
            self.play(position)
            self.update_pass_turn()

    def play(self, position):
        valid = self.game.play(position)
        if not valid:
            message = "Invalid move. It's %s's turn." % self.game.turn.color
            self.update_status(message)
        else:
            message = "%s's turn." % self.game.turn.color
            self.update_status(message)
            self.update_board()
            self.update_score()
            self.update_pass_turn()
            self.check_next_turn()

    def computer_play(self):
        # Playing Greedy
        if self.heuristic == 0:
            minimax.greedy_alpha_beta_minimax.PLAYER = self.game.turn.color
            print('------------------------------')
            print('Executing Greedy:')
            print(self.game.board)
            print(self.game.turn.color)
            print('------------------------------')
            position = minimax.greedy_alpha_beta_minimax(self.game.board,
                                                         self.depth,
                                                         self.game.turn.color, -minimax.INF, minimax.INF)[1]
            print('Greedy approach finished with choice: %s' % str(position))
            self.game.play(position)
            message = ("%s's turn." % self.game.turn.color)
            self.update_status(message)
            self.update_board()
            self.update_score()
            self.update_pass_turn()
            self.check_next_turn()
            self.update_pass_turn()
        # Playing Coin-Parity
        else:
            minimax.coinparity_alpha_beta_minimax.PLAYER = self.game.turn.color
            print('------------------------------')
            print('Executing Coin-Parity:')
            print(self.game.board)
            print(self.game.turn.color)
            print('------------------------------')
            position = minimax.coinparity_alpha_beta_minimax(self.game.board,
                                                             self.depth,
                                                             self.game.turn.color, -minimax.INF,
                                                             minimax.INF)[1]
            print('Coin-Parity approach finished with choice: %s' % str(position))
            self.game.play(position)
            message = ("%s's turn." % self.game.turn.color)
            self.update_status(message)
            self.update_board()
            self.update_score()
            self.update_pass_turn()
            self.check_next_turn()

    def check_next_turn(self):
        if self.game.is_end():
            self.update_status("End of the game.")
            self.update_board()
            self.update_score()
            self.update_pass_turn()
            self.show_end()
            self.game = False
            return
        if self.game.turn.playing_against == "COMPUTER":
            if not driver.has_valid_position(self.game.board, self.game.turn.color):
                message = "Computer passed its turn. Now it's %s's turn." % \
                          self.game.turn.color
                self.update_status(message)
                self.update_board()
                self.update_pass_turn()
                return
            else:
                self.update_status("Computers Turn")
                self.update_board()
                self.computer_play()

    def show_end(self):
        import sys
        orig_stdout = sys.stdout
        f = open('out.txt', 'a+')
        sys.stdout = f

        if self.heuristic == 0:
            print("Greedy")
        elif self.heuristic == 1:
            print("Coin Parity")
        print(self.game.board)
        print("PLayer1 score: " + str(self.game.player1.score) + ",Player2 score: " + str(self.game.player2.score))
        print("Total Nodes Visited: "+str(minimax.node_c())+"\n\n")

        sys.stdout = orig_stdout
        f.close()
        print("Node Count at the end: " + str(minimax.node_c()))
        message = "End of game. %s" % self.game.show_winner() + "\nTotal Nodes Visited: " + str(minimax.node_c())
        messagebox.showinfo(title="End", message=message)

    def update_status(self, message):
        self.status["text"] = message
        self.window.update_idletasks()

    def update_board(self):
        for row in range(8):
            for column in range(8):
                position = self.board[(row, column)]
                position["state"] = NORMAL
                #print("xxx : "+str(self.game.board[(row, column)]))
                if str(self.game.board[(row, column)]) is "W":
                    position["image"] = self.white_image
                    position.update_idletasks()
                elif str(self.game.board[(row, column)]) is "B":
                    position["image"] = self.black_image
                    position.update_idletasks()
                else:
                    position["image"] = self.empty_image
                    position.update_idletasks()
        if self.show_valid_positions:
            valid = list(driver.valid_positions(self.game.board, self.game.turn.color))
            for position in valid:
                p = self.board[position]
                p["image"] = self.valid_image
                p.update_idletasks()

    def update_score(self):
        self.score["text"] = "%s(%s): %s | %s(%s): %s" % \
                             (self.game.player1.color,
                              self.game.player1.playing_against,
                              self.game.player1.score,
                              self.game.player2.color,
                              self.game.player2.playing_against,
                              self.game.player2.score)
        self.score.update_idletasks()

    def update_pass_turn(self):
        self.pass_turn["state"] = DISABLED
        if not driver.has_valid_position(self.game.board, self.game.turn.color):
            self.pass_turn["state"] = NORMAL
            self.pass_turn.update_idletasks()

    def quit_game(self):
        if messagebox.askyesno(title="Quit", message="Are you sure you want to quit game ?"):
            quit()


class Board(dict):
    def __init__(self):
        for i in range(8):
            for j in range(8):
                self[(i, j)] = "EMPTY"

    def __str__(self):
        string = ""
        for i in range(8):
            a = ""
            for j in range(8):
                if self[(i, j)] == "EMPTY":
                    a += '-'
                else:
                    a += self[(i, j)]
            string += a + '\n'
        return string


def move(board, position, turn):
    to_change = []
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


class Game():
    def __init__(self, p1_color="W", p1_playing_against="HUMAN", p2_playing_against="COMPUTER"):
        if p1_color == "W":
            p2_color = "B"
        else:
            p2_color = "W"
        self.board = Board()
        self.player1 = Player(color=p1_color, playing_against=p1_playing_against)
        self.player2 = Player(color=p2_color, playing_against=p2_playing_against)
        self.turn = self.player1

    def start(self):
        self.board[(3, 3)] = self.board[(4, 4)] = "B"
        self.board[(3, 4)] = self.board[(4, 3)] = "W"
        self.update_scores()

    def play(self, position):
        if driver.is_valid_position(self.board, position, self.turn.color):
            move(self.board, position, self.turn.color)
            self.update_scores()
            self.change_turn()
            return True
        else:
            return False

    def update_scores(self):
        self.player1.score = driver.count_pieces(self.board, self.player1.color)
        self.player2.score = driver.count_pieces(self.board, self.player2.color)

    def change_turn(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    def show_winner(self, formatted=True):
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

    def is_end(self):
        return driver.end_game(self.board)


class Player():
    def __init__(self, color, playing_against):
        self.color = color
        self.playing_against = playing_against
        self.score = 0

if __name__ == "__main__":
    app = Othello()
