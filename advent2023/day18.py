from utils.utils import Advent
from utils.algos import neighbors
import numpy as np
from collections import deque


advent = Advent(18)


def main():
    lines = advent.get_input_lines()
    lines = parse_lines(lines)
    grid = dig_trenches(lines)
    flood_fill(grid)
    advent.submit(1, np.count_nonzero(grid == 1))


def print_grid(grid):
    lines = []
    for x in range(grid.shape[0]):
        l = ""
        for y in range(grid.shape[1]):
            l += "#" if grid[(x, y)] == 1 else "."
        lines.append(l)
    with open("grid.txt", "w") as f:
        f.write("\n".join(lines))


def parse_lines(lines):
    out = []
    for line in lines:
        dir, c, color = line.split(" ")
        out.append((dir, int(c), color))
    return out


def flood_fill(grid):
    xs = np.where(grid[:, 0] == 1)[0]
    src = (xs[len(xs) // 2], 0)

    queue = deque()
    queue.append(src)

    grid[src] = 1

    while queue:
        node = queue.popleft()

        for n in neighbors(grid, node):
            if grid[n] == 0:
                grid[n] = 1
                queue.append(n)


def dig_trenches(lines):
    grid = np.zeros((1000, 1000))
    x, y = 500, 500
    grid[(x, y)] = 1
    for dir, c, color in lines:
        if dir == "R":
            grid[x, y : y + c] = 1
            y += c
        elif dir == "L":
            grid[x, y - c : y + 1] = 1
            y -= c
        elif dir == "D":
            grid[x : x + c, y] = 1
            x += c
        elif dir == "U":
            grid[x - c : x + 1, y] = 1
            x -= c

    ones = np.where(grid == 1)
    minx = ones[0].min()
    miny = ones[1].min()
    maxx = ones[0].max()
    maxy = ones[1].max()
    return grid[minx : maxx + 1, miny : maxy + 1]


if __name__ == "__main__":
    main()
