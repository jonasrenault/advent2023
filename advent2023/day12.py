from utils.utils import Advent
from itertools import combinations
from tqdm import tqdm
from functools import lru_cache

advent = Advent(12)


def main():
    lines = advent.get_input_lines()
    lines = [l.split(" ") for l in lines]
    lines = [(s, tuple([int(x) for x in t.split(",")])) for s, t in lines]

    c = 0
    for row, broken in tqdm(lines):
        poss = arrangements(row, broken)
        for p in poss:
            if is_valid(p, broken):
                c += 1
    advent.submit(1, c)

    c = 0
    for row, broken in tqdm(lines):
        c += search("?".join([row] * 5), 0, broken * 5, 0)
        search.cache_clear()
    advent.submit(2, c)


@lru_cache
def search(row: str, idx: int, broken: tuple[int, ...], chunk_length: int) -> int:
    """
    Search number of possible combinations for row[idx:]
    given the remaining broken chunks and the current chunk length.

    Args:
        row (str): the row
        idx (int): the current index in the row
        broken (tuple[int, ...]): the remaining broken chunks
        chunk_length (int): the current broken chunk length

    Returns:
        int: the number of possible combinations
    """
    # done searching, check that last chunk has corrent length
    if idx == len(row):
        return int(
            len(broken) == 0
            and chunk_length == 0
            or len(broken) == 1
            and broken[0] == chunk_length
        )

    total = 0
    # current char is #, or ? and we try setting it to #
    if row[idx] in "#?":
        # increase length of current chunk by 1 and move to next char
        total += search(row, idx + 1, broken, chunk_length + 1)

    # current char is ., or ? and we try setting it to .
    if row[idx] in ".?":
        # no current chunk, move to next char
        if not chunk_length:
            total += search(row, idx + 1, broken, 0)
        # check current chunk has correct length and move to next char, resetting current chunk to 0
        elif len(broken) > 0 and chunk_length == broken[0]:
            total += search(row, idx + 1, broken[1:], 0)

    return total


def arrangements(row: str, broken: tuple[int, ...]) -> list[str]:
    """
    Return all possible combinations of replacing ? in row by a #.
    Not all arrangements are valid.

    Args:
        row (str): the input row
        broken (tuple[int, ...]): the list of broken chunks

    Returns:
        list[str]: possible arrangements
    """
    unknowns = [i for i, c in enumerate(row) if c == "?"]
    missing = sum(broken) - row.count("#")
    poss = []
    for switch_idx in combinations(unknowns, missing):
        p = ""
        for i, c in enumerate(row):
            if c == "?" and i in switch_idx:
                p += "#"
            elif c == "?":
                p += "."
            else:
                p += c
        poss.append(p)
    return poss


def is_valid(row: str, broken: tuple[int, ...]) -> bool:
    """
    Check if a row is valid for a given list of broken chunks.

    Args:
        row (str): the row
        broken (tuple[int, ...]): the broken chunks

    Returns:
        bool: True if all chunks of # in row have same lengths as elements of broken.
    """
    chunks = [c for c in row.split(".") if c]
    return len(chunks) == len(broken) and all(
        [len(chunk) == c for chunk, c in zip(chunks, broken)]
    )


if __name__ == "__main__":
    main()
