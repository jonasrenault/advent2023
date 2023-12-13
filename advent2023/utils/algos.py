from typing import Any
from collections import deque
from collections.abc import Sequence, Container, Iterator


deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))
deltas_8 = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def neighbors(
    grid: Sequence[Sequence[Any]], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            yield (rr, rc)


def neighbors8(
    grid: Sequence[Sequence[Any]], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas_8:
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            yield (rr, rc)


def grid_find_adjacent(
    grid: Sequence[Sequence[Any]],
    src: tuple[int, int],
    find: Container[tuple[int, int]],
) -> Iterator[tuple[tuple[int, int], int]]:
    """
    Use breadth-first search to find and yield all the nodes reachable from src,
    returning each node in find along with its distance from src

    Args:
        grid (Sequence[Sequence[Any]]): the grid
        src (tuple[int, int]): the source node
        find (Container[tuple[int, int]]): the target nodes

    Yields:
        Iterator[tuple[tuple[int, int], int]]: each target node reachable and its distance from src
    """
    visited = {src}
    queue = deque()

    for n in neighbors(grid, src):
        queue.append((1, n))

    while queue:
        dist, node = queue.popleft()
        if node not in visited:
            visited.add(node)
            if node in find:
                yield ((node), dist)
                continue

            for n in neighbors(grid, node):
                queue.append((1 + dist, n))
