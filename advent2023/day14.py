import numpy as np
import numpy.typing as npt
from tqdm import tqdm
from utils.utils import Advent

advent = Advent(14)


def main():
    lines = advent.get_input_lines()
    platform = np.array([[c for c in l] for l in lines], dtype=str)
    tiltN(platform)
    advent.submit(1, get_load(platform))

    platform = np.array([[c for c in l] for l in lines], dtype=str)
    cycle_to(1000000000, platform)
    advent.submit(2, get_load(platform))


def cycle_to(limit: int, platform: npt.NDArray[np.str_]):
    """
    Cycle to limit, finding a loop to skip steps.

    Args:
        limit (int): the limit
        platform (npt.NDArray[np.str_]): the platform
    """
    cache = {}
    start = None
    end = None
    for c in tqdm(range(limit)):
        # cycle
        tiltN(platform)
        tiltW(platform)
        tiltS(platform)
        tiltE(platform)
        # get indices of round rocks
        rocks = np.where(platform == "O")
        # check if we've seen to config already
        h = hash(tuple(r.tostring() for r in rocks))
        if h in cache:
            # if we found a loop, break and save start and end cycles of loop
            start = cache[h]
            end = c
            break
        cache[h] = c

    # if loop was found, cycle remaining steps
    if start is not None and end is not None:
        remaining = (limit - start) % (end - start) - 1
        cycle_to(remaining, platform)


def get_load(platform: npt.NDArray[np.str_]) -> int:
    """
    Compute load

    Args:
        platform (npt.NDArray[np.str_]): the platform

    Returns:
        int: the load
    """
    sx, _ = platform.shape
    return sum([sx - x for x in np.where(platform == "O")[0]])


def tiltN(platform: npt.NDArray[np.str_]):
    """
    Tilt platform to the north

    Args:
        platform (npt.NDArray[np.str_]): the platform
    """
    sx, sy = platform.shape
    for y in range(sy):
        min = 0
        for x in range(sx):
            if platform[(x, y)] == "O":
                platform[(x, y)] = "."
                platform[(min, y)] = "O"
                min += 1
            elif platform[(x, y)] == "#":
                min = x + 1


def tiltW(platform: npt.NDArray[np.str_]):
    """
    Tilt platform to the west

    Args:
        platform (npt.NDArray[np.str_]): the platform
    """
    sx, sy = platform.shape
    for x in range(sx):
        min = 0
        for y in range(sy):
            if platform[(x, y)] == "O":
                platform[(x, y)] = "."
                platform[(x, min)] = "O"
                min += 1
            elif platform[(x, y)] == "#":
                min = y + 1


def tiltS(platform: npt.NDArray[np.str_]):
    """
    Tilt platform to the south

    Args:
        platform (npt.NDArray[np.str_]): the platform
    """
    sx, sy = platform.shape
    for y in range(sy):
        min = sx - 1
        for x in range(sx - 1, -1, -1):
            if platform[(x, y)] == "O":
                platform[(x, y)] = "."
                platform[(min, y)] = "O"
                min -= 1
            elif platform[(x, y)] == "#":
                min = x - 1


def tiltE(platform: npt.NDArray[np.str_]):
    """
    Tilt platform to the east

    Args:
        platform (npt.NDArray[np.str_]): the platform
    """
    sx, sy = platform.shape
    for x in range(sx):
        min = sy - 1
        for y in range(sy - 1, -1, -1):
            if platform[(x, y)] == "O":
                platform[(x, y)] = "."
                platform[(x, min)] = "O"
                min -= 1
            elif platform[(x, y)] == "#":
                min = y - 1


if __name__ == "__main__":
    main()
