from utils.utils import Advent
import operator
from collections.abc import Callable
from math import prod


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

    ranges = {k: (1, 4000) for k in "xmas"}
    advent.submit(2, accepted_vals(rules, ranges, "in"))


def accepted_vals(
    rules: dict[
        str, list[tuple[str, Callable[[int, int], bool], int, str] | tuple[str]]
    ],
    ranges: dict[str, tuple[int, int]],
    rule: str = "in",
):
    if rule == "A":
        return prod([high - low + 1 for low, high in ranges.values()])
    if rule == "R":
        return 0

    conditions = rules[rule][:-1]
    last = rules[rule][-1][0]
    total = 0
    for rating, op, val, dest in conditions:
        low, high = ranges[rating]

        if op is operator.lt:
            if low < val:
                new_ranges = ranges | {rating: (low, val - 1)}
                total += accepted_vals(rules, new_ranges, dest)

            if high >= val:
                ranges |= {rating: (val, high)}
        else:
            if high > val:
                new_ranges = ranges | {rating: (val + 1, high)}
                total += accepted_vals(rules, new_ranges, dest)

            if low <= val:
                ranges |= {rating: (low, val)}

    total += accepted_vals(rules, ranges, last)
    return total


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
