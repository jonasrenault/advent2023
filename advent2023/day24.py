from utils.utils import Advent
from itertools import combinations

advent = Advent(24)


def main():
    lines = advent.get_input_lines()
    stones = get_stones(lines)

    total = 0
    for s1, s2 in combinations(stones, 2):
        if intersect_in_area(*s1, *s2, 200000000000000, 400000000000000):
            total += 1
    advent.submit(1, total)


def intersect_in_area(
    p1: tuple[int, int, int],
    v1: tuple[int, int, int],
    p2: tuple[int, int, int],
    v2: tuple[int, int, int],
    minx: int,
    maxx: int,
) -> bool:
    ip = line_intersection(p1, v1, p2, v2)
    if ip is None:
        return False

    x, y = ip
    if x < minx or x > maxx or y < minx or y > maxx:
        return False

    dx1 = x - p1[0]
    dx2 = x - p2[0]
    dy1 = y - p1[1]
    dy2 = y - p2[1]
    if dx1 * v1[0] < 0 or dx2 * v2[0] < 0 or dy1 * v1[1] < 0 or dy2 * v2[1] < 0:
        return False

    return True


def get_stones(
    lines: list[str],
) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    stones = []
    for line in lines:
        pos, v = line.split("@")
        pos = tuple([int(c.strip()) for c in pos.strip().split(",")])
        v = tuple([int(c.strip()) for c in v.strip().split(",")])
        stones.append((pos, v))
    return stones


def det(a: tuple[int, int], b: tuple[int, int]) -> int:
    a0, a1 = a
    b0, b1 = b
    return a0 * b1 - a1 * b0


def line_intersection(
    p1: tuple[int, int, int],
    v1: tuple[int, int, int],
    p2: tuple[int, int, int],
    v2: tuple[int, int, int],
) -> float | None:
    px1, py1, pz1 = p1
    px2, py2, pz2 = p2
    vx1, vy1, vz1 = v1
    vx2, vy2, vz2 = v2
    xdiff = (-vx1, -vx2)
    ydiff = (-vy1, -vy2)
    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (
        det((px1, py1), (px1 + vx1, py1 + vy1)),
        det((px2, py2), (px2 + vx2, py2 + vy2)),
    )
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


if __name__ == "__main__":
    main()
