from utils.utils import Advent
from collections import deque

advent = Advent(11)


def main():
    lines = advent.get_input_lines()
    grid = expand(lines)
    galaxies = find_galaxies(grid)

    distances = 0
    for idx, (sr, sc) in enumerate(galaxies):
        for dr, dc in galaxies[idx + 1 :]:
            d = abs(sr - dr) + abs(sc - dc)
            distances += d

    advent.submit(1, distances)


def neighbors(grid: list[str], node: tuple[int, int]):
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            yield (rr, rc)


def find_distances(grid, src: tuple[int, int], galaxies: list[tuple[int, int]]):
    visited = {src}
    queue = deque()

    for n in neighbors(grid, src):
        queue.append((1, n))

    while queue:
        dist, node = queue.popleft()
        if node not in visited:
            visited.add(node)
            if node in galaxies:
                yield ((node), dist)
                continue

            for n in neighbors(grid, node):
                queue.append((1 + dist, n))


def find_galaxies(grid):
    galaxies = []
    for x, row in enumerate(grid):
        for y, c in enumerate(row):
            if c != ".":
                galaxies.append((x, y))
    return galaxies


def get_empty_rows_cols(grid):
    # find empty rows and cols
    rows = list()
    cols = set()
    for r, row in enumerate(grid):
        if "#" not in row:
            rows.append(r)
        for c, ch in enumerate(row):
            if ch == "#":
                cols.add(c)

    return rows, [c for c in range(len(grid[0])) if c not in cols]


def expand(grid):
    # find empty rows and cols
    rows = list()
    cols = set()
    for r, row in enumerate(grid):
        if "#" not in row:
            rows.append(r)
        for c, ch in enumerate(row):
            if ch == "#":
                cols.add(c)

    print(
        f"empty rows: {rows}, empty cols: {[c for c in range(len(grid[0])) if c not in cols]}"
    )
    new_grid = []
    for row in grid:
        new_row = row
        new_cols = 0
        for c in range(len(row)):
            if c not in cols:
                new_row = new_row[: c + new_cols] + "." + row[c:]
                new_cols += 1
        new_grid.append(new_row)
    l = len(new_grid[0])
    for i, r in enumerate(rows):
        new_grid.insert(r + i, "." * l)

    return new_grid


if __name__ == "__main__":
    main()
