from tqdm import tqdm
import numpy as np
from utils.utils import Advent

advent = Advent(16)

DIRS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

MIRRORS = {
    "/": {"^": ">", ">": "^", "v": "<", "<": "v"},
    "\\": {"^": "<", ">": "v", "v": ">", "<": "^"},
}

SPLITTERS = {"-": ("<", ">"), "|": ("^", "v")}


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in l] for l in lines], dtype=str)
    activated = propagate(grid, (0, 0), ">")
    activated = set([n for n, _ in activated])
    advent.submit(1, len(activated))

    advent.submit(2, find_config(grid))


def find_config(grid):
    res = 0
    for x in range(grid.shape[0]):
        activated = propagate(grid, (x, 0), ">")
        res = max(res, len(set([n for n, _ in activated])))
        activated = propagate(grid, (x, grid.shape[1] - 1), "<")
        res = max(res, len(set([n for n, _ in activated])))

    for y in range(grid.shape[0]):
        activated = propagate(grid, (0, y), "v")
        res = max(res, len(set([n for n, _ in activated])))
        activated = propagate(grid, (grid.shape[0] - 1, y), "^")
        res = max(res, len(set([n for n, _ in activated])))
    return res


def propagate(grid, start, dir):
    seen = set()
    beams = set(
        [
            (
                start,
                dir,
            )
        ]
    )
    while len(beams) != 0:
        node, dir = beams.pop()
        seen.add((node, dir))
        new_beams = next_tiles(grid, node, dir)
        for b in new_beams:
            if b not in seen:
                beams.add(b)
    return seen


def next_tiles(grid, node, dir):
    tile = grid[node]
    tiles = []
    if tile == ".":
        neighbor = node[0] + DIRS[dir][0], node[1] + DIRS[dir][1]
        tiles.append((neighbor, dir))
    if tile == "\\" or tile == "/":
        next_dir = MIRRORS[tile][dir]
        neighbor = node[0] + DIRS[next_dir][0], node[1] + DIRS[next_dir][1]
        tiles.append((neighbor, next_dir))
    if tile == "-" or tile == "|":
        if dir in SPLITTERS[tile]:
            neighbor = node[0] + DIRS[dir][0], node[1] + DIRS[dir][1]
            tiles.append((neighbor, dir))
        else:
            for next_dir in SPLITTERS[tile]:
                neighbor = node[0] + DIRS[next_dir][0], node[1] + DIRS[next_dir][1]
                tiles.append((neighbor, next_dir))

    tiles = [
        (n, d)
        for n, d in tiles
        if 0 <= n[0] < grid.shape[0] and 0 <= n[1] < grid.shape[1]
    ]
    return tiles


if __name__ == "__main__":
    main()
