import env
import numpy as np
import pickle

# TODO: make state work regardless of player 1 or 2
class Player:
    def __init__(self, token, epsilon=0.3):
        self.token = token
        self.epsilon = epsilon  # epsilon-greedy
        self.lr = 0.2  # learning rate
        self.gamma = 0.95  # decay

        self.states = []  # set of states taken in this game
        self.states_value = {}  # dict of values given to particular states

    def reset(self):
        self.states = []

    def move(self, board):
        positions = board.open_positions()
        # decide what move to take
        if np.random.uniform() < self.epsilon:
            # random action
            position = np.random.choice(positions)
        else:
            # predict best move
            best_outcome = -999
            for p in positions:
                # make a copy of the board
                test_board = env.Board()
                test_board._grid = board.state()
                # try the move
                test_board.move(self.token, p)
                outcome = (
                    0
                    if self.states_value.get(test_board.state()) is None
                    else self.states_value.get(test_board.state())
                )
                if outcome >= best_outcome:
                    best_outcome = outcome
                    position = p

        # make the move
        board.move(self.token, position)
        self.states.append(board.state())

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
            self.p1.give_reward(0.5)
            self.p2.give_reward(0.5)

    def play_match(self):
        while not self.board.complete:
            # player one's move
            self.p1.move(self.board)
            if self.board.complete:
                break
            # player two's move
            self.p2.move(self.board)

        self.reward(self.p1, self.p2)

    def play(self, rounds=1000):
        for _ in range(rounds):
            self.play_match()
            self.board.reset()
            self.p1.reset()
            self.p2.reset()
