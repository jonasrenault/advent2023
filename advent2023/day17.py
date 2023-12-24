import heapq
from collections import defaultdict
from collections.abc import Iterator
from math import inf

import numpy as np
import numpy.typing as npt
from utils.utils import Advent

advent = Advent(17)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[int(c) for c in l] for l in lines], dtype=int)
    advent.submit(1, find_path(grid, (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1)))
    advent.submit(
        2, find_path(grid, 4, 10, (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1))
    )


def find_path(
    grid: npt.NDArray[np.int_],
    min_step: int,
    max_step: int,
    src: tuple[int, int],
    dst: tuple[int, int],
) -> int:
    queue = [(0, (src, True)), (0, (src, False))]
    distances = defaultdict(lambda: inf)
    visited = set()

    while queue:
        dist, (node, vertical) = heapq.heappop(queue)

        if node == dst:
            return dist

        if (node, vertical) in visited:
            continue

        visited.add((node, vertical))

        for neighbor, weight in neighbors(grid, (node, vertical), min_step, max_step):
            distance = dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return inf


def line_step(
    grid: npt.NDArray[np.int_],
    min_step: int,
    max_step: int,
    r: int,
    c: int,
    dr: int,
    dc: int,
) -> Iterator[tuple[tuple[int, int], int]]:
    weight = 0
    maxr = grid.shape[0] - 1
    maxc = grid.shape[1] - 1
    rr = r
    rc = c
    for step in range(1, max_step + 1):
        rr += dr
        rc += dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            weight += grid[rr, rc]
            if min_step <= step:
                yield ((rr, rc), weight)


def neighbors(
    grid: npt.NDArray[np.int_],
    node: tuple[int, int],
    min_step: int,
    max_step: int,
) -> Iterator[tuple[tuple[tuple[int, int], bool], int]]:
    (r, c), vertical = node

    if vertical:
        for coords, weight in line_step(grid, min_step, max_step, r, c, -1, 0):
            yield (coords, not vertical), weight
        for coords, weight in line_step(grid, min_step, max_step, r, c, 1, 0):
            yield (coords, not vertical), weight
    else:
        for coords, weight in line_step(grid, min_step, max_step, r, c, 0, -1):
            yield (coords, not vertical), weight
        for coords, weight in line_step(grid, min_step, max_step, r, c, 0, 1):
            yield (coords, not vertical), weight


if __name__ == "__main__":
    main()
