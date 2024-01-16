from utils.utils import Advent
import numpy as np
import numpy.typing as npt
from collections.abc import Iterator

advent = Advent(21)

deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in l] for l in lines], dtype=str)
    start = np.where(grid == "S")
    start = start[0][0], start[1][0]
    nodes = {start}
    for i in range(64):
        nodes = step(grid, nodes)
    advent.submit(1, len(nodes))


def neighbors(
    grid: npt.NDArray[np.str_], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc and grid[(rr, rc)] != "#":
            yield (rr, rc)


def step(
    grid: npt.NDArray[np.str_], nodes: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    next_nodes = set()
    for node in nodes:
        for neighbor in neighbors(grid, node):
            next_nodes.add(neighbor)
    return next_nodes


if __name__ == "__main__":
    main()
