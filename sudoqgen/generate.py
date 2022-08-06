import numpy as np
import random

def pattern(r, c, base, side):
    return (base * (r % base) + r // base + c) % side


def shuffle(s):
    return random.sample(s, len(s))


def generate_sudoku(difficulty=45, base: int = 3):
    """Generate a sudoku grid with valid values

    Args:
        difficulty(int, optional): the number of tiles to be removed. Defaults to 45.
        base (int, optional): the base of the sudoku. Defaults to 3.

    Returns:
        list: the generated board
    """
    side = base * base

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(
        range(1, base * base + 1)
    )  # produce board using randomized baseline pattern
    solved = np.array([[nums[pattern(r, c, base, side)] for c in cols] for r in rows])

    # remove a given amound of tiles
    sudoku = solved.copy()
    tiles_remaining = [(i, j) for i in range(side) for j in range(side)]
    to_remove = random.sample(tiles_remaining, difficulty)

    for (i, j) in to_remove:
        sudoku[i][j] = 0

    data = {
        "sudoku": sudoku,
        "solved": solved,
    }

    return data
