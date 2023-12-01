from utils.utils import Advent

advent = Advent(1)

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def calibration(lines: list[str]) -> int:
    calibration = [tuple(c for c in l if c.isdigit()) for l in lines]
    calibration = [int(c[0] + c[-1]) for c in calibration]
    return sum(calibration)


def main():
    lines = advent.get_input_lines()
    advent.submit(1, calibration(lines))

    input = advent.get_input()
    for k, v in DIGITS.items():
        input = input.replace(k, k + v + k)
    lines = list(map(lambda l: l.strip(), input.rstrip("\n").split("\n")))
    advent.submit(2, calibration(lines))


if __name__ == "__main__":
    main()
