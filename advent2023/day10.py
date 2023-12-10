from utils.utils import Advent
import numpy as np
import numpy.typing as npt

advent = Advent(10)


PIPES = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}

tbl = str.maketrans("|-LJ7F", "│─└┘┐┌")


def main():
    lines = advent.get_input_lines()
    grid = [[c for c in l] for l in lines]
    grid = np.array(grid, dtype=str)
    loop = get_loop(grid)
    advent.submit(1, int(len(loop) / 2))

    # replace everything not in loop with .
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if (x, y) not in loop:
                grid[x][y] = "."

    # Count number of points inside polygon
    count = 0
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if is_point_inside_polygon(grid, x, y):
                count += 1
                grid[x][y] = "X"

    for x in range(grid.shape[0]):
        print("".join(grid[x]).translate(tbl))
    advent.submit(2, count)


def get_loop(grid: npt.NDArray[np.str_]) -> list[tuple[int, int]]:
    """
    Starting from S position, follow the pipes until we loop back to S.
    Since we don't know what S is, try out all of its neighbors until
    we loop back to S, or until an exception is raised in which case
    no loop was found.

    Args:
        grid (npt.NDArray[np.str_]): the grid

    Returns:
        list[tuple[int, int]]: the loop
    """
    S = np.where(grid == "S")
    S = S[0][0], S[1][0]
    for x, y in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        loop = [S]
        current = (S[0] + x, S[1] + y)
        try:
            while grid[current] != "S":
                loop.append(current)
                current = next_pipe(grid, current, loop[-2])
        except ValueError:
            continue
        else:
            return loop


def next_pipe(
    grid: npt.NDArray[np.str_], current: tuple[int, int], previous: tuple[int, int]
) -> tuple[int, int]:
    """
    Follow the pipes from the current position, returning the next position.

    Args:
        grid (npt.NDArray[np.str_]): the
        current (tuple[int, int]): the current pos
        previous (tuple[int, int]): the previous pos

    Raises:
        ValueError: if current position is out of bounds
        ValueError: if current position is not a pipe
        ValueError: if current position cannot be reached from previous position

    Returns:
        tuple[int, int]: the next position
    """
    shape_x, shape_y = grid.shape
    if not (0 <= current[0] < shape_x and 0 <= current[1] < shape_y):
        raise ValueError(f"{current} position is out of bounds.")

    pipe = grid[current]
    if pipe == "." or pipe == "S":
        raise ValueError(f"{current} position is not a pipe.")
    from_direction = (previous[0] - current[0], previous[1] - current[1])
    if from_direction not in PIPES[pipe]:
        raise ValueError(f"{previous} position is not connected to {current}")
    to_direction = [d for d in PIPES[pipe] if d != from_direction][0]
    return (current[0] + to_direction[0], current[1] + to_direction[1])


def intersections(grid: npt.NDArray[np.str_], x: int, y: int) -> int:
    """
    Count the # of intersections by drawing a line to the right
    of the point.
    Intersections are |, or any other section of pipe which is not
    horizontal (i.e L---J or F---7).

    Args:
        grid (npt.NDArray[np.str_]): grid where only pipes are different from .
        x (int): the start x
        y (int): the start y

    Returns:
        int: the number of intersections
    """
    count = 0
    last = None
    for i in range(y + 1, grid.shape[1]):
        current = grid[(x, i)]
        if current == "|":
            count += 1
        elif current not in ".-":
            if last is None:
                last = current
            else:
                if not (
                    (last == "F" and current == "7") or (last == "L" and current == "J")
                ):
                    count += 1
                last = None

    return count


def is_point_inside_polygon(grid: npt.NDArray[np.str_], x: int, y: int) -> bool:
    """
    Check if point is inside polygon

    Args:
        grid (npt.NDArray[np.str_]): the
        x (int): point x
        y (int): point y

    Returns:
        bool: True if point is inside polygon
    """
    # return False if point is part of loop (is not a dot)
    if grid[(x, y)] != ".":
        return False

    # Count intersections of the polygon edges with a horizontal
    # line going through the test point
    count = intersections(grid, x, y)
    if count % 2 == 1:
        return True
    return False


if __name__ == "__main__":
    main()
