from utils.utils import Advent

advent = Advent(9)


def main():
    lines = advent.get_input_lines()
    histories = [[int(x.strip()) for x in l.split(" ")] for l in lines]
    advent.submit(1, sum([forward(h) for h in histories]))
    advent.submit(2, sum([backward(h) for h in histories]))


def get_offsets(history: list[int]):
    diffs = []
    current = history
    while not all([x == 0 for x in current]):
        diff = [current[i] - current[i - 1] for i in range(1, len(current))]
        diffs.append(diff)
        current = diff

    return diffs


def forward(history: list[int]):
    offsets = get_offsets(history)
    x = 0
    for offset in offsets[::-1]:
        x += offset[-1]
    return history[-1] + x


def backward(history: list[int]):
    offsets = get_offsets(history)
    x = 0
    for offset in offsets[::-1]:
        x = offset[0] - x
    return history[0] - x


if __name__ == "__main__":
    main()
