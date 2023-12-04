from utils.utils import Advent

advent = Advent(4)


def main():
    lines = advent.get_input_lines()
    score = 0
    for line in lines:
        winning, draw = line[line.index(":") + 2 :].split("|")
        winning = set([int(x.strip()) for x in winning.split(" ") if x])
        draw = set([int(x.strip()) for x in draw.split(" ") if x])
        won = winning & draw
        if won:
            score += pow(2, len(won) - 1)
    advent.submit(1, score)

    copies = {}
    for idx, line in enumerate(lines):
        if idx not in copies:
            copies[idx] = 1
        winning, draw = line[line.index(":") + 2 :].split("|")
        winning = set([int(x.strip()) for x in winning.split(" ") if x])
        draw = set([int(x.strip()) for x in draw.split(" ") if x])
        won = winning & draw
        if won:
            for x in range(idx + 1, idx + 1 + len(won)):
                copies[x] = copies.get(x, 1) + copies[idx]
    advent.submit(2, sum(copies.values()))


if __name__ == "__main__":
    main()
