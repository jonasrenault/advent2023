from __future__ import annotations
from utils.utils import Advent
from itertools import product
from collections import defaultdict, deque
from string import ascii_uppercase


advent = Advent(22)


class Brick:
    ids = product(ascii_uppercase, repeat=3)

    def __init__(self, start: tuple[int, int, int], end: tuple[int, int, int]) -> None:
        cubes = []
        for i in range(len(start)):
            if start[i] != end[i]:
                for x in range(min(start[i], end[i]), max(start[i], end[i]) + 1):
                    cubes.append(
                        (
                            x if i == 0 else start[0],
                            x if i == 1 else start[1],
                            x if i == 2 else start[2],
                        )
                    )
        if not cubes:
            cubes.append(start)
        self.cubes = cubes
        self.id = "".join(next(Brick.ids))

    @property
    def min_height(self) -> int:
        return min([z for _, _, z in self.cubes])

    @property
    def max_height(self) -> int:
        return max([z for _, _, z in self.cubes])

    def set_height(self, height: int) -> int:
        mh = self.min_height
        self.cubes = [(x, y, height + z - mh) for (x, y, z) in self.cubes]

    def overlaps(self, other: Brick) -> bool:
        for l, r in product(self.cubes, other.cubes):
            if l[0] == r[0] and l[1] == r[1]:
                return True
        return False

    def supports(self, other: Brick) -> bool:
        if self.max_height != other.min_height - 1:
            return False
        return self.overlaps(other)

    def __repr__(self) -> str:
        return self.id + ": " + " ".join([str(c) for c in self.cubes])


def main():
    lines = advent.get_input_lines()
    bricks = get_bricks(lines)
    bricks.sort(key=lambda x: x.min_height)
    fall_bricks(bricks)
    supported_by, supports = get_supports(bricks)
    removable = get_removable(bricks, supported_by)
    advent.submit(1, len(removable))

    to_remove = set([b.id for b in bricks]) - removable
    total = 0
    for b in to_remove:
        total += len(get_falling(b, supported_by, supports)) - 1
    advent.submit(2, total)


def get_falling(
    removed_brick: str, supported_by: dict[str, set[str]], supports: dict[str, set[str]]
) -> set[str]:
    """
    Get the bricks that would fall if you remove given brick

    Args:
        removed_brick (str): the brick to remove
        supported_by (dict[str, set[str]]): supported_by dict
        supports (dict[str, set[str]]): supports dict

    Returns:
        set[str]: ids of bricks that would fall, including removed_brick
    """
    falling = set()
    queue = deque([removed_brick])

    while queue:
        brick = queue.popleft()
        falling.add(brick)
        for supported in supports[brick]:
            if all([b in falling for b in supported_by[supported]]):
                queue.append(supported)

    return falling


def get_supports(
    bricks: list[Brick],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """
    Get dicts of which bricks support / are supported by which other bricks

    Args:
        bricks (list[Brick]): list of bricks

    Returns:
        tuple[dict[str, set[str]], dict[str, set[str]]]: dicts of supported_by and supports
    """
    # for each brick, find which other bricks it rests on
    supported_by = defaultdict(set)
    for i in range(len(bricks)):
        brick = bricks[i]
        for ob in bricks[:i]:
            if ob.supports(brick):
                supported_by[brick.id].add(ob.id)

    # invert the dict to find out for each brick which other bricks it supports
    supports = defaultdict(set)
    for brick, on_top in supported_by.items():
        for ob in on_top:
            supports[ob].add(brick)

    return supported_by, supports


def get_removable(bricks: list[Brick], supported_by: dict[str, set[str]]) -> set[Brick]:
    """
    Find bricks which can be safely removed

    Args:
        bricks (list[Brick]): the list of bricks

    Returns:
        set[Brick]: set of bricks which can be removed
    """
    # any brick can be deleted unless it supports another brick by itself
    removable = set([b.id for b in bricks])
    for values in supported_by.values():
        if len(values) == 1:
            removable.discard(values.pop())
    return removable


def fall_bricks(bricks: list[Brick]):
    """
    Make bricks fall to their lowest possible height

    Args:
        bricks (list[Brick]): list of bricks
    """
    # for each brick
    for i in range(len(bricks)):
        brick = bricks[i]
        # if it's already on the floor, leave it
        if brick.min_height == 1:
            continue

        # else, find bricks below which overlap with it
        below = set()
        for ob in bricks[:i]:
            if brick.overlaps(ob):
                below.add(ob)
        if below:
            # set height of brick to max height of bricks below + 1
            brick.set_height(max([b.max_height for b in below]) + 1)
        else:
            # if no brick was found, it rests on the floor
            brick.set_height(1)


def get_bricks(lines: list[str]) -> list[Brick]:
    bricks = []
    for line in lines:
        left, right = line.split("~")
        left = left.split(",")
        right = right.split(",")
        left = tuple([int(x) for x in left])
        right = tuple([int(x) for x in right])
        bricks.append(Brick(left, right))
    return bricks


if __name__ == "__main__":
    main()
