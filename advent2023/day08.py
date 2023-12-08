import math
from functools import reduce
from typing import Callable

from utils.utils import Advent

advent = Advent(8)


def main():
    lines = advent.get_input_lines()
    instructions = lines[0].strip()
    nodes = {}
    for line in lines[2:]:
        if line:
            key, values = line.split("=")
            values = tuple(values.replace(")", "").replace("(", "").split(","))
            nodes[key.strip()] = tuple([v.strip() for v in values])

    steps = reach_end(nodes, "AAA", instructions, lambda x: x == "ZZZ")
    advent.submit(1, steps)

    starts = {key for key in nodes.keys() if key[-1] == "A"}
    steps = {
        key: reach_end(nodes, key, instructions, lambda x: x[-1] == "Z")
        for key in starts
    }
    advent.submit(2, reduce(lcm, steps.values()))


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def reach_end(
    nodes: dict[str, tuple[str, str]],
    start: str,
    instructions: str,
    stop: Callable[[str], bool],
):
    current = start
    idx = 0
    while not stop(current):
        instruction = instructions[idx % len(instructions)]
        current = next_node(nodes, instruction, current)
        idx += 1
    return idx


def next_node(nodes: dict[str, tuple[str, str]], instruction: str, node: str):
    return nodes[node][0] if instruction == "L" else nodes[node][1]


if __name__ == "__main__":
    main()
