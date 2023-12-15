from tqdm import tqdm
from utils.utils import Advent

advent = Advent(15)


def main():
    lines = advent.get_input_lines()
    steps = lines[0].split(",")
    hashes = [to_hash(s) for s in steps]
    advent.submit(1, sum(hashes))


def to_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


if __name__ == "__main__":
    main()
