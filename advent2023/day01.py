import re

with open("advent2023/input.txt", "r") as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

calibration = [tuple(c for c in l if c in "123456789") for l in lines]
calibration = [int(c[0] + c[-1]) for c in calibration]
print(sum(calibration))

with open("advent2023/input.txt", "r") as f:
    puzzle = f.read()

digits = {
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
for k, v in digits.items():
    puzzle = puzzle.replace(k, k + v + k)

lines = puzzle.split("\n")
lines = [l.strip() for l in lines]
calibration = [tuple(c for c in l if c in "123456789") for l in lines]
calibration = [int(c[0] + c[-1]) for c in calibration]
print(calibration)
print(sum(calibration))
