import numpy as np
import numpy.typing as npt
from utils.utils import Advent

advent = Advent(14)


def main():
    lines = advent.get_input_lines()
    platform = np.array([[c for c in l] for l in lines], dtype=str)
    tilt(platform)
    advent.submit(1, get_load(platform))


def get_load(platform: npt.NDArray[np.str_]):
    sx, sy = platform.shape
    return sum([sx - x for x in np.where(platform == "O")[0]])


def tilt(platform: npt.NDArray[np.str_]):
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
    return platform


if __name__ == "__main__":
    main()
