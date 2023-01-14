from games import *
from tkinter import *
#from TicTacToe5x5 import *
import os
import sys
import numpy as np

################### PYRAMID TIC TAC TOE GAME ##########################
size = 3
k = 3
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'

class Tic_Tac_Toe_Pyramid(Game):

    def __init__(self):
        self.size = size
        self.k = k
        moves = []
        num = 2
        for x in range(1, size + 1):
            for y in range(1, num):
                moves.append((x, y))
            num = num + 2
        self.initial = GameState(to_move="X", utility=0, board={}, moves=moves)

        # GUI
        self.window = Tk()
        self.window.title('Tic-Tac-Toe Pyramid')
        self.canvas = Canvas(self.window, width=1000, height=600)
        self.canvas.pack()

        self.initialize_board()

        self.player_X_turns = True

        Button(
            self.window,
            text='Exit',
            command=lambda:self.window.destroy()
        ).pack(expand=True)


    def mainloop(self):
        self.window.mainloop()


    def initialize_board(self):
        self.canvas.create_line(400, 0, 400, 600)
        self.canvas.create_line(600, 0, 600, 600)
        self.canvas.create_line(200, 200, 200, 600)
        self.canvas.create_line(800, 200, 800, 600)
        self.canvas.create_line(200, 200, 800, 200)
        self.canvas.create_line(0, 400, 1000, 400)


    def result(self, state, move):
        if move not in state.moves:
            return state
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)

        return GameState(to_move=("O" if state.to_move == "X" else "X"),
                         utility=self.compute_utility(board, move, state.to_move), board=board, moves=moves)


    def actions(self, state):
        return state.moves


    def terminal_test(self, state):
        if len(state.moves) == 0 or state.utility != 0:
            return True
        return False


    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility


    def to_move(self, state):
        return state.to_move

    def compute_utility(self, board, move, player):
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1)) or
                self.k_in_row(board, move, player, (1, 2)) or
                self.k_in_row(board, move, player, (-1, -2))):
                return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        # mainloop()
        while True:
            for player in players:
                move = player(self, state)
                print("move:" + str(move))
                print("player:" + str(state.to_move))

                if state.to_move == "X":
                    self.player_X_turns = True
                else:
                    self.player_X_turns = False

                self.draw_position(move)
                state = self.result(state, move)
                print("board:" + str(state.board))

                if state.to_move == "X":
                    self.player_X_turns = True
                else:
                    self.player_X_turns = False

                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


    def draw_O(self, move):
        if move[0] == 1:
            self.canvas.create_oval(420, 20, 580, 180, width=symbol_thickness,outline=symbol_O_color)
        if move[0] == 2:
            if move[1] == 3:
                self.canvas.create_oval(620, 220, 780, 380, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 2:
                self.canvas.create_oval(420, 220, 580, 380, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 1:
                self.canvas.create_oval(220, 220, 380, 380, width=symbol_thickness,outline=symbol_O_color)
        if move[0] == 3:
            if move[1] == 5:
                self.canvas.create_oval(820, 420, 980, 580, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 4:
                self.canvas.create_oval(620, 420, 780, 580, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 3:
                self.canvas.create_oval(420, 420, 580, 580, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 2:
                self.canvas.create_oval(220, 420, 380, 580, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 1:
                self.canvas.create_oval(20, 420, 180, 580, width=symbol_thickness,outline=symbol_O_color)


    def draw_X(self, move):
        if move[0] == 1:
            self.canvas.create_line(420, 20, 580, 180, width=symbol_thickness, fill=symbol_X_color)
            self.canvas.create_line(420, 180, 580, 20, width=symbol_thickness, fill=symbol_X_color)
        if move[0] == 2:
            if move[1] == 1:
                self.canvas.create_line(220, 220, 380, 380, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(220, 380, 380, 220, width=symbol_thickness, fill=symbol_X_color)
            if move[1] == 2:
                self.canvas.create_line(420, 220, 580, 380, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(420, 380, 580, 220, width=symbol_thickness, fill=symbol_X_color)
            if move[1] == 3:
                self.canvas.create_line(620, 220, 780, 380, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(620, 380, 780, 220, width=symbol_thickness, fill=symbol_X_color)
        if move[0] == 3:
            if move[1] == 1:
                self.canvas.create_line(20, 420, 180, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(20, 580, 180, 420, width=symbol_thickness, fill=symbol_X_color)
            if move[1] == 2:
                self.canvas.create_line(220, 420, 380, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(220, 580, 380, 420, width=symbol_thickness, fill=symbol_X_color)
            if move[1] == 3:
                self.canvas.create_line(420, 420, 580, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(420, 580, 580, 420, width=symbol_thickness, fill=symbol_X_color)
            if move[1] == 4:
                self.canvas.create_line(620, 420, 780, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(620, 580, 780, 420, width=symbol_thickness, fill=symbol_X_color)
            if move[1] == 5:
                self.canvas.create_line(820, 420, 980, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(820, 580, 980, 420, width=symbol_thickness, fill=symbol_X_color)


    def draw_position(self, move):
        if self.player_X_turns == True:
            self.draw_X(move)
        else:
            self.draw_O(move)

################### 3X3 TIC TAC TOE GAME ##########################

class Tic_Tac_Toe(Game):

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

        # GUI
        self.window = Tk()
        self.window.title('Tic-Tac-Toe Pyramid')
        self.canvas = Canvas(self.window, width=600, height=600)
        self.canvas.pack()

        self.initialize_board()

        self.player_X_turns = True

        Button(
            self.window,
            text='Exit',
            command=lambda:self.window.destroy()
        ).pack(expand=True)


    def mainloop(self):
        self.window.mainloop()


    def initialize_board(self):
        self.canvas.create_line(200, 0, 200, 600)
        self.canvas.create_line(400, 0, 400, 600)
        self.canvas.create_line(200, 200, 200, 600)
        self.canvas.create_line(200, 400, 600, 400)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0


    def to_move(self, state):
        return state.to_move

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0


    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        # mainloop()
        while True:
            for player in players:
                move = player(self, state)
                print("move:" + str(move))
                print("player:" + str(state.to_move))

                if state.to_move == "X":
                    self.player_X_turns = True
                else:
                    self.player_X_turns = False

                self.draw_position(move)
                state = self.result(state, move)
                print("board:" + str(state.board))

                if state.to_move == "X":
                    self.player_X_turns = True
                else:
                    self.player_X_turns = False

                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


    def draw_O(self, move):
        if move[0] == 1:
            if move[1] == 3:
                self.canvas.create_oval(420, 20, 580, 180, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 2:
                self.canvas.create_oval(220, 20, 380, 180, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 1:
                self.canvas.create_oval(20, 20, 180, 180, width=symbol_thickness,outline=symbol_O_color)
        if move[0] == 2:
            if move[1] == 3:
                self.canvas.create_oval(420, 220, 580, 380, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 2:
                self.canvas.create_oval(220, 220, 380, 380, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 1:
                self.canvas.create_oval(20, 220, 180, 380, width=symbol_thickness,outline=symbol_O_color)
        if move[0] == 3:
            if move[1] == 3:
                self.canvas.create_oval(420, 420, 580, 580, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 2:
                self.canvas.create_oval(220, 420, 380, 580, width=symbol_thickness,outline=symbol_O_color)
            if move[1] == 1:
                self.canvas.create_oval(20, 420, 180, 580, width=symbol_thickness,outline=symbol_O_color)


    def draw_X(self, move):
        if move[0] == 1:
            if move[1] == 3:
                self.canvas.create_line(420, 20, 580, 180, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(420, 180, 580, 20, width=symbol_thickness, fill=symbol_X_color)

            if move[1] == 2:
                self.canvas.create_line(220, 20, 380, 180, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(220, 180, 380, 20, width=symbol_thickness, fill=symbol_X_color)

            if move[1] == 1:
                self.canvas.create_line(20, 20, 180, 180, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(20, 180, 180, 20, width=symbol_thickness, fill=symbol_X_color)

        if move[0] == 2:
            if move[1] == 3:
                self.canvas.create_line(420, 220, 580, 380, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(420, 380, 580, 220, width=symbol_thickness, fill=symbol_X_color)

            if move[1] == 2:
                self.canvas.create_line(220, 220, 380, 380, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(220, 380, 380, 220, width=symbol_thickness, fill=symbol_X_color)

            if move[1] == 1:
                self.canvas.create_line(20, 220, 180, 380, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(20, 380, 180, 220, width=symbol_thickness, fill=symbol_X_color)

        if move[0] == 3:
            if move[1] == 3:
                self.canvas.create_line(420, 420, 580, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(420, 580, 580, 420, width=symbol_thickness, fill=symbol_X_color)

            if move[1] == 2:
                self.canvas.create_line(220, 420, 380, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(220, 580, 380, 420, width=symbol_thickness, fill=symbol_X_color)

            if move[1] == 1:
                self.canvas.create_line(20, 420, 180, 580, width=symbol_thickness, fill=symbol_X_color)
                self.canvas.create_line(20, 580, 180, 480, width=symbol_thickness, fill=symbol_X_color)


    def draw_position(self, move):
        if self.player_X_turns == True:
            self.draw_X(move)
        else:
            self.draw_O(move)

####################################################

if __name__ == "__main__":
    game_level = ''
    while game_level != 'E' and game_level != 'M' and game_level != 'H':
        try:
            game_level = input('Please choose game level?[Easy(E)/Medium(M)/Hard(H)]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    if game_level == 'E':
        game_instance = Tic_Tac_Toe() #TicTacToe()  # Creating the game instance
    elif game_level == 'M':
        game_instance = Tic_Tac_Toe_Pyramid()
    elif game_level == 'H':
        os.system("TicTacToe5x5.py 1")

    print(
        game_instance.initial.moves)  # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2,1), (2, 2), (2, 3), (3, 1)]

    utility = game_instance.play_game(alpha_beta_player, query_player)  # computer moves first
    if (utility < 0):
        print("\n O won the game")
        sys.exit()
    else:
        print("\n X won the game")
        sys.exit()

    game_instance.mainloop()