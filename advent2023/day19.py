from utils.utils import Advent
import operator
from collections.abc import Callable


advent = Advent(19)


def main():
    lines = advent.get_input_lines()
    rules, parts = parse_input(lines)

    ratings = 0
    for part in parts:
        dest = apply_rules(rules, part, rules["in"])
        if dest == "A":
            ratings += sum(part.values())
    advent.submit(1, ratings)


def apply_rules(
    rules: dict[
        str, list[tuple[str, Callable[[int, int], bool], int, str] | tuple[str]]
    ],
    part: dict[str, int],
    conditions: list[tuple[str, Callable[[int, int], bool], int, str] | tuple[str]],
) -> str:
    for condition in conditions:
        if len(condition) == 1:
            dest = condition[0]
            if dest in rules:
                return apply_rules(rules, part, rules[dest])
            return dest
        rating, op, val, dest = condition
        if op(part[rating], val):
            if dest in rules:
                return apply_rules(rules, part, rules[dest])
            return dest


def parse_input(
    lines: list[str],
) -> tuple[
    dict[str, list[tuple[str, Callable[[int, int], bool], int, str] | tuple[str]]],
    list[dict[str, int]],
]:
    is_rule = True
    rules = {}
    parts = []
    for line in lines:
        if not line:
            is_rule = False
        elif is_rule:
            name, conditions = parse_rule(line)
            rules[name] = conditions
        else:
            parts.append(parse_part(line))
    return rules, parts


def parse_rule(
    line: str,
) -> tuple[str, list[tuple[str, Callable[[int, int], bool], int, str] | tuple[str]]]:
    name = line[: line.index("{")]
    rules = line[line.index("{") + 1 : -1]
    rules = rules.split(",")
    conditions = []
    for rule in rules:
        if ":" not in rule:
            conditions.append((rule,))
        else:
            rating = rule[0]
            op = operator.lt if rule[1] == "<" else operator.gt
            val = int(rule[2 : rule.index(":")])
            dest = rule[rule.index(":") + 1 :]
            conditions.append((rating, op, val, dest))
    return name, conditions


def parse_part(line: str) -> dict[str, int]:
    ratings = line[1:-1].split(",")
    part = {rating[0]: int(rating[2:]) for rating in ratings}
    return part


if __name__ == "__main__":
    main()
