import numpy as np
import random
import sys
import io

sys.path.append(".")
import env


def test_state():
    b = env.Board()
    expect = np.zeros((3, 3))
    a = b.state() == expect
    assert a.all()
    coords = [(i, j) for i in range(3) for j in range(3)]
    random.shuffle(coords)
    for row, col in coords:
        b.move(1, row, col)
        expect[row, col] = 1
        a = b.state() == expect
        assert a.all()
    b.reset()
    a = b.state() == np.zeros((3, 3))
    assert a.all()


def test_move():
    b = env.Board()
    r = b.move(0, 1, 1)
    assert r == -1
    r = b.move(0, 3, 1)
    assert r == -1
    r = b.move(2, 1, 1)
    assert r == 0
    r = b.move(1, 1, 1)
    assert r == -1
    r = b.move(1, 0, 0)
    assert r == 0
    r = b.move("o", 0, 1)
    assert r == 0
    r = b.move("O", 0, 2)
    assert r == 0
    r = b.move("x", 1, 0)
    assert r == 0
    r = b.move("X", 1, 2)
    assert r == 0


def test_draw():
    b = env.Board()
    b.move("x", 0, 0)
    b.move("o", 1, 1)
    b.move("x", 1, 2)
    b.move("o", 2, 0)
    b.move("x", 0, 2)

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    b.draw()
    sys.stdout = old_stdout

    printed = buffer.getvalue()
    expect = " X |   | X \n---+---+---\n   | O | X \n---+---+---\n O |   |   \n"
    print(expect)
    print(printed)
    assert expect == printed
