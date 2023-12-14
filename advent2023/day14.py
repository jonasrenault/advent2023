import numpy as np
import numpy.typing as npt
from utils.utils import Advent

advent = Advent(14)


def main():
    lines = advent.get_input_lines()
    platform = np.array([[c for c in l] for l in lines], dtype=str)
    # tilt(platform)
    # advent.submit(1, get_load(platform))
    print(platform)
    fixed = np.where(platform == "#")
    tilt(platform, fixed, "N")
    print(platform)


def get_load(platform: npt.NDArray[np.str_]):
    sx, sy = platform.shape
    return sum([sx - x for x in np.where(platform == "O")[0]])


# def tilt(platform: npt.NDArray[np.str_]):
#     sx, sy = platform.shape
#     for y in range(sy):
#         min = 0
#         for x in range(sx):
#             if platform[(x, y)] == "O":
#                 platform[(x, y)] = "."
#                 platform[(min, y)] = "O"
#                 min += 1
#             elif platform[(x, y)] == "#":
#                 min = x + 1
#     return platform


def tilt(platform: npt.NDArray[np.str_], fixed, dir: str):
    sx, sy = platform.shape

    # North
    rocks = np.where(platform == "O")
    platform[rocks] = "."
    for y in set(rocks[1]):
        fixed_x = fixed[0][fixed[1] == y]
        fixed_x.sort()
        if 0 not in fixed_x:
            fixed_x = np.insert(fixed_x, 0, 0)
        round = rocks[0][rocks[1] == y]
        for x in fixed_x[::-1]:
            c = np.sum(round >= x)
            if c:
                platform[x + 1 : x + 1 + c, y] = "O"
    # for y in range(sy):
    #     min = 0
    #     for x in range(sx):
    #         if platform[(x, y)] == "O":
    #             platform[(x, y)] = "."
    #             platform[(min, y)] = "O"
    #             min += 1
    #         elif platform[(x, y)] == "#":
    #             min = x + 1
    # return platform


if __name__ == "__main__":
    main()
