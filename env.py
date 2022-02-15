import numpy as np


class Board:
    """
    model a noughts and crosses board
    """

    def __init__(self):
        self.O = 1
        self.X = 2
        self.grid = np.zeros((3, 3))  # define grid coordinates from top left

    def reset(self):
        self.grid = np.zeros((3, 3))

    def move(self, token, row, col):
        if self.grid[row, col] != 0:
            return -1
        if token == self.O or token == "O" or token == "o":
            self.grid[row, col] = self.O
            return 0
        if token == self.X or token == "X" or token == "X":
            self.grid[row, col] = self.X
            return 0
        return -1

    def state(self):
        return self.grid

    def draw(self):
        token_line = list("   |   |   ")
        in_between = "---+---+---"
        for row in range(3):
            line = token_line.copy()
            for col in range(3):
                if self.grid[row][col] == self.O:
                    line[1 + col * 4] = "O"
                if self.grid[row][col] == self.X:
                    line[1 + col * 4] = "X"
            print("".join(line))
            if row < 2:
                print(in_between)
