from utils.utils import Advent
import numpy as np


advent = Advent(18)


def main():
    lines = advent.get_input_lines()
    moves = parse_moves(lines)
    distance, vertices = trenches(moves)
    advent.submit(1, int(1 + (distance / 2) + poly_area(vertices)))

    moves = parse_moves(lines, True)
    distance, vertices = trenches(moves)
    advent.submit(2, int(1 + (distance / 2) + poly_area(vertices)))


def poly_area(vertices: list[tuple[int, int]]) -> float:
    """
    Compute area of polygon given its vertices using Shoelace formula.

    Args:
        vertices (list[tuple[int, int]]): polygon vertices as list of x, y coordinates

    Returns:
        float: the polygon area
    """
    x = np.array([x for x, _ in vertices[:-1]], dtype=int)
    y = np.array([y for _, y in vertices[:-1]], dtype=int)
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def parse_moves(lines: list[str], part2: bool = False) -> list[tuple[str, int]]:
    """
    Parse moves

    Args:
        lines (list[str]): the input lines
        part2 (bool, optional): whether to parse hex codes as moves. Defaults to False.

    Returns:
        list[tuple[str, int]]: list of moves (dir, distance)
    """
    out = []
    dirs = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for line in lines:
        dir, distance, color = line.split(" ")
        distance = int(distance)
        if part2:
            distance = int(color[2:-2], 16)
            dir = dirs[color[-2]]
        out.append((dir, distance))
    return out


def trenches(moves: list[tuple[str, int]]) -> tuple[int, list[tuple[int, int]]]:
    """
    Dig trenches for given moves

    Args:
        moves (list[tuple[str, int]]): the moves

    Returns:
        tuple[int, list[tuple[int, int]]]: the distance of the trenches, and the list of its vertices
    """
    x, y = 0, 0
    vertices = [(x, y)]
    distance = 0
    for dir, dist in moves:
        if dir == "R":
            y += dist
        elif dir == "L":
            y -= dist
        elif dir == "D":
            x += dist
        elif dir == "U":
            x -= dist
        vertices.append((x, y))
        distance += dist
    return distance, vertices


if __name__ == "__main__":
    main()
