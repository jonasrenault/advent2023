import sys
from collections import defaultdict, deque
from collections.abc import Iterator

import numpy as np
import numpy.typing as npt
from utils.utils import Advent

advent = Advent(23)

deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))
sys.setrecursionlimit(10**6)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in l] for l in lines], dtype=str)
    h, w = grid.shape
    start = (0, np.where(grid[0, :] == ".")[0][0])
    end = (h - 1, np.where(grid[h - 1, :] == ".")[0][0])

    graph = grid_to_graph(grid, start, end, False)
    best = longest_path(graph, end, start, 0, set())
    print(best)
    # advent.submit(1, dfs(grid, start, end))

    graph = grid_to_graph(grid, start, end, True)
    best = longest_path(graph, end, start, 0, set())
    print(best)

    # print(dfs(grid, start, end, False))


def grid_to_graph(
    grid: npt.NDArray[np.str_],
    src: tuple[int, int],
    end: tuple[int, int],
    ignore_slopes: bool = False,
) -> dict[tuple[int, int], set[tuple[int, int]]]:
    """
    Transform grid to a graph. If ignore_slopes is True, slopes are ignored
    and graph is simplified by merging nodes that have only two neighbors,
    keeping only intersections as nodes

    Args:
        grid (npt.NDArray[np.str_]): the grid
        src (tuple[int, int]): the starting position
        end (tuple[int, int]): the end position
        ignore_slopes (bool, optional): ignore slopes. Defaults to False.

    Returns:
        dict[tuple[int, int], set[tuple[int, int]]]: the graph
    """
    graph = defaultdict(set)
    seen = set()
    queue = deque([src])

    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)

        if ignore_slopes:
            for n, weight in adjacent_nodes(grid, node, src, end):
                graph[node].add((n, weight))
                queue.append(n)
        else:
            for n in neighbors(grid, node):
                graph[node].add((n, 1))
                queue.append(n)

    return graph


def adjacent_nodes(
    grid: npt.NDArray[np.str_],
    curr: tuple[int, int],
    src: tuple[int, int],
    end: tuple[int, int],
) -> Iterator[tuple[tuple[int, int], int]]:
    """
    Yield the adjacent nodes and their distance from the curr position. Nodes
    are grid positions that are either the start or end, or that have more than
    2 neighbors

    Args:
        grid (npt.NDArray[np.str_]): the grid
        curr (tuple[int, int]): the current pos
        src (tuple[int, int]): the start pos
        end (tuple[int, int]): the end pos

    Yields:
        Iterator[tuple[tuple[int, int], int]]: iterator of nodes, distance
    """
    queue = [(curr, 0)]
    visited = set()

    while queue:
        node, dist = queue.pop()
        visited.add(node)

        for n in neighbors(grid, node, True):
            if n in visited:
                continue

            if is_node(grid, n, src, end, True):
                yield n, dist + 1
                continue

            queue.append((n, dist + 1))


def is_node(
    grid: npt.NDArray[np.str_],
    node: tuple[int, int],
    src: tuple[int, int],
    end: tuple[int, int],
    ignore_slopes: bool,
) -> bool:
    """
    Check if node position is a node in the graph, i.e. is the start or end pos, or
    has more than two neighbors

    Args:
        grid (npt.NDArray[np.str_]): the grid
        node (tuple[int, int]): the curr pos
        src (tuple[int, int]): the start pos
        end (tuple[int, int]): the end pos
        ignore_slopes (bool): ignore slopes

    Returns:
        bool: true if curr node is a node
    """
    return (
        node == src
        or node == end
        or len(list(neighbors(grid, node, ignore_slopes))) > 2
    )


def neighbors(
    grid: npt.NDArray[np.str_], node: tuple[int, int], ignore_slopes: bool = False
) -> Iterator[tuple[int, int]]:
    """
    Iterator for the neighbors of given node

    Args:
        grid (npt.NDArray[np.str_]): the grid
        node (tuple[int, int]): the node
        ignore_slopes (bool, optional): ignore_slopes. Defaults to False.

    Yields:
        Iterator[tuple[int, int]]: Iterator of neighbor positions
    """
    r, c = node
    maxr = grid.shape[0] - 1
    maxc = grid.shape[1] - 1
    cell = grid[node]

    if cell == "." or ignore_slopes:
        for dr, dc in deltas_4:
            rr, rc = r + dr, c + dc
            if 0 <= rr <= maxr and 0 <= rc <= maxc and grid[rr, rc] != "#":
                yield (rr, rc)
    elif cell == ">":
        yield (r, c + 1)
    elif cell == "v":
        yield (r + 1, c)


def longest_path(
    graph: dict[tuple[int, int], set[tuple[int, int]]],
    end: tuple[int, int],
    curr: tuple[int, int],
    dist: int,
    seen: set[tuple[int, int]],
) -> int:
    """
    Find the longest path in the graph, from curr position to end, given dist
    and traversed nodes to reach curr position

    Args:
        graph (dict[tuple[int, int], set[tuple[int, int]]]): the graph
        end (tuple[int, int]): the end position
        curr (tuple[int, int]): the curr position
        dist (int): distance to reach curr position
        seen (set[tuple[int, int]]): nodes traversed to reach curr position

    Returns:
        int: the longest path
    """
    if curr == end:
        return dist

    best = 0
    seen.add(curr)

    for n, weight in graph[curr]:
        if n in seen:
            continue
        best = max(best, longest_path(graph, end, n, dist + weight, seen))

    seen.remove(curr)
    return best


if __name__ == "__main__":
    main()
