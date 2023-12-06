from utils.utils import Advent

advent = Advent(6)


def main():
    lines = advent.get_input_lines()
    times = [int(x.strip()) for x in lines[0][len("Time: ") :].split(" ") if x]
    distances = [int(x.strip()) for x in lines[1][len("Distance: ") :].split(" ") if x]

    solutions = 1
    for time, distance in zip(times, distances):
        traveled = [charge * (time - charge) for charge in range(time)]
        wins = sum([1 for c in traveled if c > distance])
        solutions *= wins
    advent.submit(1, solutions)

    time = int(lines[0][len("Time: ") :].replace(" ", ""))
    distance = int(lines[1][len("Distance: ") :].replace(" ", ""))

    mint = None
    maxt = None
    for charge in range(time):
        traveled = charge * (time - charge)
        if traveled > distance:
            mint = charge
            break

    for charge in range(time, 0, -1):
        traveled = charge * (time - charge)
        if traveled > distance:
            maxt = charge
            break

    advent.submit(2, maxt - mint + 1)


if __name__ == "__main__":
    main()
