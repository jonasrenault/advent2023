import math
from functools import reduce
from typing import Callable

from utils.utils import Advent

advent = Advent(8)

INSTRUCTION_KEYS = {"L": 0, "R": 1}


def main():
    lines = advent.get_input_lines()
    instructions = lines[0].strip()
    nodes = {}
    for line in lines[2:]:
        if line:
            key, values = line.split("=")
            values = tuple(values.replace(")", "").replace("(", "").split(","))
            nodes[key.strip()] = tuple([v.strip() for v in values])

    steps = reach_end(nodes, instructions, "AAA", lambda x: x == "ZZZ")
    advent.submit(1, steps)

    starts = {key for key in nodes.keys() if key[-1] == "A"}
    steps = {
        key: reach_end(nodes, instructions, key, lambda x: x[-1] == "Z")
        for key in starts
    }
    advent.submit(2, reduce(lcm, steps.values()))


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def reach_end(
    nodes: dict[str, tuple[str, str]],
    instructions: str,
    start: str,
    stop: Callable[[str], bool],
):
    current = start
    idx = 0
    while not stop(current):
        instruction = instructions[idx % len(instructions)]
        current = nodes[current][INSTRUCTION_KEYS[instruction]]
        idx += 1
    return idx


if __name__ == "__main__":
    main()
