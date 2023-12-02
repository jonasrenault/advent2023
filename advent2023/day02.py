import re
from utils.utils import Advent
from itertools import chain

advent = Advent(2)

game = {"red": 12, "green": 13, "blue": 14}


def parse_game(line: str):
    id = re.search("Game (\d+)", line).group(1)
    draws = line[line.index(":") + 1 :].split(";")
    impossible = [is_impossible(d) for d in draws]
    return id, any(impossible)


def is_impossible(draw: str):
    counts = draw.split(",")
    for c in counts:
        for k, v in game.items():
            if k in c:
                count = int(c.replace(k, "").strip())
                if count > v:
                    return True


def main():
    lines = advent.get_input_lines()
    games = [parse_game(l) for l in lines]
    impossible_games = [int(id) for (id, imp) in games if not imp]
    advent.submit(1, sum(impossible_games))


if __name__ == "__main__":
    main()
