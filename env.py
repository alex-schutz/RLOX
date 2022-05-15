import numpy as np

GRID_SIZE = 3


class Board:
    """
    model a noughts and crosses board state
    O represented by 1
    X represented by -1
    No token represented by 0

      |   |
    ---------
      |   |
    ---------
      |   |

    """

    def __init__(self):
        self.O = 1
        self.X = -1
        self._grid = np.zeros(
            (GRID_SIZE, GRID_SIZE)
        )  # define grid coordinates from top left
        self.complete = False

    def reset(self):
        self.complete = False
        self._grid = np.zeros((GRID_SIZE, GRID_SIZE))

    def move(self, token, position):
        if position[0] not in range(GRID_SIZE) or position[1] not in range(GRID_SIZE):
            return -1
        if not self.is_open(position):
            return -1
        if token == self.O or token == "O" or token == "o":
            self._grid[position] = self.O
            self.evaluate()
            return 0
        if token == self.X or token == "X" or token == "x":
            self._grid[position] = self.X
            self.evaluate()
            return 0
        return -1

    def state(self):
        return self._grid.copy()

    def draw(self):
        token_line = list("   |   |   ")
        in_between = "---+---+---"
        for row in range(GRID_SIZE):
            line = token_line.copy()
            for col in range(GRID_SIZE):
                if self._grid[row][col] == self.O:
                    line[1 + col * 4] = "O"
                if self._grid[row][col] == self.X:
                    line[1 + col * 4] = "X"
            print("".join(line))
            if row < 2:
                print(in_between)

    def is_open(self, pos):
        return self._grid[pos] == 0

    def open_positions(self):
        # return a list of open positions on the grid
        pos = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.is_open((i, j)):
                    pos.append((i, j))
        return pos

    def evaluate(self):
        # Evaluate the state of the board. Return -1 for X win, 1 for O win, 0 for draw (if self.complete == True)

        # check rows/cols
        if GRID_SIZE in np.sum(self._grid, 0) or GRID_SIZE in np.sum(self._grid, 1):
            self.complete = True
            return 1

        if -GRID_SIZE in np.sum(self._grid, 0) or -GRID_SIZE in np.sum(self._grid, 1):
            self.complete = True
            return -1

        # check diagonals
        if GRID_SIZE in [np.trace(self._grid), np.trace(np.fliplr(self._grid))]:
            self.complete = True
            return 1

        if -GRID_SIZE in [np.trace(self._grid), np.trace(np.fliplr(self._grid))]:
            self.complete = True
            return -1

        if self.open_positions() == []:
            self.complete = True
            return 0

        self.complete = False
        return None
