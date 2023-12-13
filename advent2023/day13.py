import numpy as np
import numpy.typing as npt
from tqdm import tqdm
from utils.utils import Advent
from collections.abc import Iterator

advent = Advent(13)


def main():
    lines = advent.get_input_lines()
    patterns = get_patterns(lines)

    summaries = [get_mirror(p) for p in patterns]
    advent.submit(1, sum(summaries))

    fixed_s = []
    for i, p in tqdm(enumerate(patterns)):
        for c in switch_one(p):
            s = get_mirror(c, summaries[i])
            if s:
                fixed_s.append(s)
                break
    advent.submit(2, sum(fixed_s))


def switch_one(pattern: npt.NDArray[np.str_]) -> Iterator[npt.NDArray[np.str_]]:
    """
    Switch one of the values of pattern

    Args:
        pattern (npt.NDArray[np.str_]): the pattern

    Yields:
        Iterator[npt.NDArray[np.str_]]: iterator over switched patterns
    """
    for x in range(pattern.shape[0]):
        for y in range(pattern.shape[1]):
            c = np.copy(pattern)
            if c[x, y] == "#":
                c[x, y] = "."
            else:
                c[x, y] = "#"
            yield c


def get_mirror(pattern: npt.NDArray[np.str_], avoid: int | None = None) -> int | None:
    """
    Return summary value of mirror col or row in pattern, avoiding value if given

    Args:
        pattern (npt.NDArray[np.str_]): the pattern
        avoid (int | None, optional): value to avoid. Defaults to None.

    Returns:
        int | None: the mirror summary value
    """
    for col in range(1, pattern.shape[1]):
        if is_mirror_col(pattern, col) and (avoid is None or avoid != col):
            return col

    for row in range(1, pattern.shape[0]):
        if is_mirror_row(pattern, row) and (avoid is None or avoid != row * 100):
            return row * 100


def get_patterns(lines: list[str]) -> list[npt.NDArray[np.str_]]:
    """
    Parse patterns

    Args:
        lines (list[str]): input lines

    Returns:
        list[npt.NDArray[np.str_]]: list of patterns
    """
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


def is_mirror_col(pattern: npt.NDArray[np.str_], col: int) -> bool:
    """
    Check if col is a mirror col (right most)

    Args:
        pattern (npt.NDArray[np.str_]): the pattern
        col (int): the rightmost pattern of a potential mirror

    Returns:
        bool: True if is mirror
    """
    j = 1
    while 0 <= (col - j) and (col + j - 1) < pattern.shape[1]:
        if not np.all(pattern[:, col - j] == pattern[:, col + j - 1]):
            return False
        j += 1
    return True


def is_mirror_row(pattern: npt.NDArray[np.str_], row: int) -> bool:
    """
    Check if row is a mirror row (bottom most)

    Args:
        pattern (npt.NDArray[np.str_]): the pattern
        row (int): the lower row of a potential mirror

    Returns:
        bool: True if row is mirror row
    """
    j = 1
    while 0 <= (row - j) and (row + j - 1) < pattern.shape[0]:
        if not np.all(pattern[row - j, :] == pattern[row + j - 1, :]):
            return False
        j += 1
    return True


if __name__ == "__main__":
    main()
