from utils.utils import Advent
import numpy as np
import numpy.typing as npt
from collections.abc import Iterator
from collections import deque, defaultdict
import math
import heapq


advent = Advent(23)

deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))
forbidden_slopes = {(-1, 0): "v", (0, -1): ">", (0, 1): "<", (1, 0): "^"}


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in l] for l in lines], dtype=str)
    h, w = grid.shape
    start = (0, np.where(grid[0, :] == ".")[0][0])
    end = (h - 1, np.where(grid[h - 1, :] == ".")[0][0])

    advent.submit(1, dfs(grid, start, end))


def neighbors(
    grid: npt.NDArray[np.str_], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = grid.shape[0] - 1
    maxc = grid.shape[1] - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if (
            0 <= rr <= maxr
            and 0 <= rc <= maxc
            and grid[rr, rc] != "#"
            and grid[rr, rc] != forbidden_slopes[(dr, dc)]
        ):
            yield (rr, rc)


def dfs(
    grid: npt.NDArray[np.str_],
    src: tuple[int, int],
    end: tuple[int, int],
) -> int:
    queue = [(0, src)]
    visited = set()
    best = 0

    while queue:
        dist, node = queue.pop()
        if dist == -1:
            visited.remove(node)
            continue

        if node == end:
            best = max(best, dist)
            continue

        if node in visited:
            continue

        visited.add(node)
        queue.append((-1, node))
        for n in neighbors(grid, node):
            queue.append((dist + 1, n))

    return best


def dijkstra(
    grid: npt.NDArray[np.str_],
    src: tuple[int, int],
    end: tuple[int, int],
) -> int:
    distance = defaultdict(lambda: math.inf, {src: 0})
    queue = [(0, src)]
    visited = set()

    while queue:
        dist, node = heapq.heappop(queue)

        if node == end:
            return -dist

        if node not in visited:
            visited.add(node)

            for n in neighbors(grid, node):
                new_dist = dist - 1

                if new_dist < distance[n]:
                    distance[n] = new_dist
                    heapq.heappush(queue, (new_dist, n))


def grid_find_adjacent(
    grid: npt.NDArray[np.str_],
    src: tuple[int, int],
    find: set[tuple[int, int]],
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


if __name__ == "__main__":
    main()
