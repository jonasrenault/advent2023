from utils.utils import Advent
from itertools import combinations
from tqdm import tqdm

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


def arrangements(row: str, broken: tuple[int, ...]) -> list[str]:
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
    chunks = [c for c in row.split(".") if c]
    return len(chunks) == len(broken) and all(
        [len(chunk) == c for chunk, c in zip(chunks, broken)]
    )


if __name__ == "__main__":
    main()
