from utils.utils import Advent
import numpy as np

advent = Advent(3)

DIRS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def main():
    puzzle = advent.get_input_lines()
    number_indices = get_number_indices(puzzle)
    parts = [get_number(puzzle, i) for i in number_indices if is_part(puzzle, i)]
    advent.submit(1, sum(parts))


def get_number_indices(puzzle: list[list[str]]) -> list[tuple[int, int, int]]:
    """
    Find row and start, stop indices of numbers in puzzle
    """
    numbers = list()

    for i in range(len(puzzle)):
        line = puzzle[i]
        start = None
        for j in range(len(line)):
            c = line[j]
            if c.isdigit():
                if start is None:
                    start = j
            elif start is not None:
                numbers.append((i, start, j - 1))
                start = None
        if start is not None:
            numbers.append((i, start, len(line) - 1))

    return numbers


def is_part(puzzle: list[list[str]], index: tuple[int, int, int]) -> bool:
    """
    Check whether number is a part.
    """
    i, j, k = index
    for x in range(j, k + 1):
        for a, b in DIRS:
            if (
                0 <= i + a < len(puzzle)
                and 0 <= x + b < len(puzzle[0])
                and puzzle[i + a][x + b] != "."
                and not puzzle[i + a][x + b].isdigit()
            ):
                return True
    return False


def get_number(puzzle: list[list[str]], index: tuple[int, int, int]) -> int:
    """
    Get number value.
    """

    i, j, k = index
    return int(puzzle[i][j : k + 1])


if __name__ == "__main__":
    main()
