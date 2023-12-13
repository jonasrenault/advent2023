from utils.utils import Advent
import numpy as np
import numpy.typing as npt

advent = Advent(13)


def main():
    lines = advent.get_input_lines()
    patterns = get_patterns(lines)

    summary = [get_mirror(p) for p in patterns]
    summary = [x for x in summary if x]
    advent.submit(1, sum(summary))


def get_mirror(pattern):
    for col in range(1, pattern.shape[1]):
        if is_mirror_col(pattern, col):
            return col

    for row in range(1, pattern.shape[0]):
        if is_mirror_row(pattern, row):
            return row * 100


def get_patterns(lines: list[str]) -> list[npt.NDArray[np.str_]]:
    patterns = []
    pattern = []
    for line in lines:
        if line:
            pattern.append([c for c in line])
        else:
            patterns.append(np.array(pattern, dtype=str))
            pattern = []
    patterns.append(np.array(pattern, dtype=str))
    return patterns


def is_mirror_col(pattern, col):
    j = 1
    while 0 <= (col - j) and (col + j - 1) < pattern.shape[1]:
        if not np.all(pattern[:, col - j] == pattern[:, col + j - 1]):
            return False
        j += 1
    return True


def is_mirror_row(pattern, row):
    j = 1
    while 0 <= (row - j) and (row + j - 1) < pattern.shape[0]:
        if not np.all(pattern[row - j, :] == pattern[row + j - 1, :]):
            return False
        j += 1
    return True


if __name__ == "__main__":
    main()
