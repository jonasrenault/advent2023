from utils.utils import Advent

advent = Advent(10)


PIPES = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}


def main():
    lines = advent.get_input_lines()
    grid = [[c for c in l] for l in lines]
    shape_x, shape_y = len(grid), len(grid[0])
    S = None
    for x in range(shape_x):
        for y in range(shape_y):
            if grid[x][y] == "S":
                S = (x, y)
                break
        if S:
            break

    for x, y in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        loop = [S]
        current = (S[0] + x, S[1] + y)
        current_s = grid[current[0]][current[1]]
        try:
            while current_s != "S":
                loop.append(current)
                current = next_pipe(grid, current, loop[-2])
                current_s = grid[current[0]][current[1]]
        except ValueError:
            continue
        else:
            advent.submit(1, int(len(loop) / 2))
            break


def next_pipe(grid, current: tuple[int, int], previous: tuple[int, int]):
    shape_x, shape_y = len(grid), len(grid[0])
    if not (0 <= current[0] < shape_x and 0 <= current[1] < shape_y):
        raise ValueError(f"{current} position is out of bounds.")

    pipe = grid[current[0]][current[1]]
    if pipe == "." or pipe == "S":
        raise ValueError(f"{current} position is not a pipe.")
    from_direction = (previous[0] - current[0], previous[1] - current[1])
    if from_direction not in PIPES[pipe]:
        raise ValueError(f"{previous} position is not connected to {current}")
    to_direction = [d for d in PIPES[pipe] if d != from_direction][0]
    return (current[0] + to_direction[0], current[1] + to_direction[1])


if __name__ == "__main__":
    main()
