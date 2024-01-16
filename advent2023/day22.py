from __future__ import annotations
from utils.utils import Advent
from itertools import product
from collections import defaultdict
from uuid import uuid4
from string import ascii_letters


advent = Advent(22)


class Brick:
    count = 0

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
        self.id = str(uuid4())
        # self.id = ascii_letters[Brick.count]
        # Brick.count += 1

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
    bricks.sort(key=lambda x: x.min_height)
    print(bricks)
    # print(bricks)
    # print(len(count_deletable(bricks)))
    # advent.submit(1, len(count_deletable(bricks)))


def count_deletable(bricks):
    # find which bricks support which
    supports = defaultdict(set)
    for i in range(len(bricks)):
        brick = bricks[i]
        for ob in bricks[:i]:
            if ob.supports(brick):
                supports[brick.id].add(ob.id)

    # any brick can be deleted unless it supports another brick alone
    deletable = set([b.id for b in bricks])
    for values in supports.values():
        if len(values) == 1:
            try:
                deletable.remove(values.pop())
            except KeyError:
                pass
    return deletable


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

        # find any brick below it which overlaps with it
        for ob in bricks[:i][::-1]:
            if brick.overlaps(ob):
                # set the new height as this brick's max height + 1
                brick.set_height(ob.max_height + 1)
                break
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
        diff = 0
        for l, r in zip(left, right):
            if l != r:
                diff += 1
        if diff > 1:
            print(line)
        bricks.append(Brick(left, right))
    return bricks


if __name__ == "__main__":
    main()
