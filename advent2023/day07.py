from utils.utils import Advent
from collections import Counter
from functools import cmp_to_key

advent = Advent(7)

CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
CARDS_JOKER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
TYPES = ["HIGH", "ONE", "TWO", "THREE", "FULL", "FOUR", "FIVE"]


def main():
    lines = advent.get_input_lines()
    hands = [tuple(l.strip().split(" ")) for l in lines]
    hands = [(tuple(c for c in h), int(b)) for (h, b) in hands]

    sorted_hands = sorted(hands, key=cmp_to_key(hand_bet_compare))
    winnings = [(idx + 1) * h[1] for idx, h in enumerate(sorted_hands)]
    advent.submit(1, sum(winnings))

    sorted_joker_hands = sorted(hands, key=cmp_to_key(hand_bet_compare_joker))
    winnings = [(idx + 1) * h[1] for idx, h in enumerate(sorted_joker_hands)]
    advent.submit(2, sum(winnings))


def hand_type(hand: tuple[str], joker: bool = False):
    c = Counter(hand)
    if joker:
        jokers = c.get("J", 0)
        del c["J"]
    else:
        jokers = 0
    most_common = c.most_common(2)
    mc1 = most_common[0][1] if len(most_common) > 0 else 0
    mc2 = most_common[1][1] if len(most_common) > 1 else 0
    if mc1 + jokers == 5:
        return TYPES.index("FIVE")
    if mc1 + jokers == 4:
        return TYPES.index("FOUR")
    if mc1 + jokers == 3 and mc2 == 2:
        return TYPES.index("FULL")
    if mc1 + jokers == 3:
        return TYPES.index("THREE")
    if mc1 + jokers == 2 and mc2 == 2:
        return TYPES.index("TWO")
    if mc1 + jokers == 2:
        return TYPES.index("ONE")
    return TYPES.index("HIGH")


def hand_bet_compare(left: tuple[tuple[str], int], right: tuple[tuple[str], int]):
    return hand_compare(left[0], right[0])


def hand_bet_compare_joker(left: tuple[tuple[str], int], right: tuple[tuple[str], int]):
    return hand_compare(left[0], right[0], True)


def hand_compare(left: tuple[str], right: tuple[str], joker: bool = False):
    left_type = hand_type(left, joker)
    right_type = hand_type(right, joker)
    if left_type != right_type:
        return left_type - right_type
    for l, r in zip(left, right):
        if l != r:
            return (
                CARDS.index(l) - CARDS.index(r)
                if not joker
                else CARDS_JOKER.index(l) - CARDS_JOKER.index(r)
            )
    return 0


if __name__ == "__main__":
    main()
