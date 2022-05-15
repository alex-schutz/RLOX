#!/usr/bin/python3

import game

if __name__ == "__main__":
    g = game.NoughtsAndCrosses()
    g.add_players(game.Player, game.Player)
    g.play()

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
