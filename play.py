#!/usr/bin/python3

import game

if __name__ == "__main__":
    g = game.NoughtsAndCrosses()
    g.add_players(game.Player, game.Player)
    g.play()
