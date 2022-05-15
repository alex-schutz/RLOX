import env
import numpy as np
import pickle


class HumanPlayer:
    def __init__(self, token):
        self.token = token

    def reset(self):
        pass

    def give_reward(self, r):
        pass

    def move(self, board):
        print("Choose a position")
        board.draw()
        print()
        r = -1
        while r != 0:
            row = int(input("Row:")) - 1
            col = int(input("Col:")) - 1
            r = board.move(self.token, (row, col))
            if r != 0:
                print("Invalid, try again")
        print()
        board.draw()
        print()


# TODO: make state work regardless of player 1 or 2
class Player:
    def __init__(self, token, epsilon=0.3):
        self.token = token
        self.epsilon = epsilon  # epsilon-greedy
        self.decay_epsilon = 0.999  # epsilon decay rate
        self.lr = 0.2  # learning rate
        self.gamma = 0.95  # decay

        self.states = []  # set of states taken in this game
        self.states_value = {}  # dict of values given to particular states

    def reset(self):
        self.states = []
        self.epsilon = self.decay_epsilon * self.epsilon

    def state_hash(self, state):
        # store board state as string, with own state stored as O
        me = 1 if (self.token == "o" or self.token == "O") else -1

        st = state.flatten()
        h = ""
        for i in st:
            if i == me:
                h += "O"
            elif i == -me:
                h += "X"
            else:
                h += "_"
        return h

    def board_hash(self, board):
        # find the hash of the board state, unique to rotation/reflection
        st = board.state()
        hashes = []

        # rotate
        for _ in range(4):
            hashes.append(self.state_hash(st))
            st = np.rot90(st)
        # reflect and rotate
        st = np.fliplr(st)
        for _ in range(4):
            hashes.append(self.state_hash(st))
            st = np.rot90(st)

        # alphabetically first hash identifies unique hash
        hashes.sort()
        return hashes[0]

    def move(self, board):
        positions = board.open_positions()
        # decide what move to take
        if np.random.uniform() < self.epsilon:
            # random action
            position = positions[np.random.choice(len(positions))]
        else:
            # predict best move
            best_outcome = -999
            for p in positions:
                # make a copy of the board
                test_board = env.Board()
                test_board._grid = board.state()
                # try the move
                test_board.move(self.token, p)
                h = self.board_hash(test_board)
                outcome = (
                    0 if self.states_value.get(h) is None else self.states_value.get(h)
                )
                if outcome >= best_outcome:
                    best_outcome = outcome
                    position = p

        # make the move
        board.move(self.token, position)
        self.states.append(self.board_hash(board))

    def give_reward(self, reward):
        # update the values assigned to each board state
        # V(s_t) = V(s_t) + alpha*[gamma*V(s_{t+1}) - V(s_t)]

        for st in reversed(self.states):  # backpropagate
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (
                self.gamma * reward - self.states_value[st]
            )
            reward = self.states_value[st]

    def save_policy(self):
        f = open("policy_" + str(self.token), "wb")
        pickle.dump(self.states_value, f)
        f.close()

    def load_policy(self, file):
        f = open(file, "rb")
        self.states_value = pickle.load(f)
        f.close()


class NoughtsAndCrosses:
    def __init__(self):
        self.board = env.Board()

    def add_players(self, p1, p2):
        self.p1 = p1("o")
        self.p2 = p2("x")

    def change_players(self, p1=None, p2=None):
        if p1 is not None:
            self.p1 = p1("o")
        if p2 is not None:
            self.p2 = p2("x")

    def reward(self):
        winner = self.board.evaluate()

        if winner == 1:
            self.p1.give_reward(1)
            self.p2.give_reward(0)

        if winner == -1:
            self.p1.give_reward(0)
            self.p2.give_reward(1)

        # try varying these weights so that ties are less desirable
        if winner == 0:
            self.p1.give_reward(0.2)
            self.p2.give_reward(0.5)

    def play_match(self):
        while not self.board.complete:
            # player one's move
            r = self.p1.move(self.board)
            if self.board.complete:
                break
            # player two's move
            self.p2.move(self.board)

        self.reward()

    def play(self, rounds=1000):
        for i in range(rounds):
            self.play_match()
            if (i % 100) == 0:
                print(f"round {i+1}/{rounds}")
                self.board.draw()
                print()
            self.board.reset()
            self.p1.reset()
            self.p2.reset()
