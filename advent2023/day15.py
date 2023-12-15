from tqdm import tqdm
from utils.utils import Advent
from collections import defaultdict

advent = Advent(15)


def main():
    lines = advent.get_input_lines()
    steps = lines[0].split(",")
    hashes = [to_hash(s) for s in steps]
    advent.submit(1, sum(hashes))

    boxes = defaultdict(list)
    for s in tqdm(steps):
        apply_step(s, boxes)
    advent.submit(2, get_power(boxes))


def get_power(boxes: defaultdict[int, list[str]]) -> int:
    power = 0
    for b, lenses in boxes.items():
        power += (b + 1) * sum([(i + 1) * l[1] for i, l in enumerate(lenses)])
    return power


def apply_step(step: str, boxes: defaultdict[int, list[str]]):
    if "=" in step:
        op = "="
    else:
        op = "-"
    label = step[: step.index(op)]
    box = to_hash(label)

    lenses = boxes[box]
    lensei = [i for i, l in enumerate(lenses) if l[0] == label]

    if op == "-" and len(lensei) == 1:
        del boxes[box][lensei[0]]
    elif op == "=" and len(lensei) == 1:
        boxes[box][lensei[0]] = (label, int(step[step.index(op) + 1 :]))
    elif op == "=":
        boxes[box].append((label, int(step[step.index(op) + 1 :])))


def to_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


if __name__ == "__main__":
    main()
