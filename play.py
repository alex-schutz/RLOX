#!/usr/bin/python3

import game
import os

if __name__ == "__main__":
    diffs = ["easy", "medium", "hard"]
    d = ""
    while d not in diffs:
        d = input(f"Select difficulty ({', '.join(diffs)}): ")

    g = game.NoughtsAndCrosses()
    g.add_players(game.Player, game.Player)

    pol = f"policy_{d}1"
    if not os.path.exists(pol):
        # train the players
        g.play(rounds=(diffs.index(d) + 1) * 400)
        g.save_policy(pol)

    g.load_policy(pol)
    g.change_players(p1=game.HumanPlayer)
    g.play_match()
    g.board.draw()
    w = g.board.evaluate()
    if w == 1:
        print("You win!")
    elif w == -1:
        print("You lose!")
    else:
        print("Tie!")
