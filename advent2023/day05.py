from utils.utils import Advent

advent = Advent(5)

MAPS: dict[str, dict[tuple[int, int], int]] = {
    "seed-to-soil": {},
    "soil-to-fertilizer": {},
    "fertilizer-to-water": {},
    "water-to-light": {},
    "light-to-temperature": {},
    "temperature-to-humidity": {},
    "humidity-to-location": {},
}


def main():
    lines = advent.get_input_lines()
    seeds = read_puzzle(lines)
    locations = []
    for seed in seeds:
        src = seed
        for key in MAPS.keys():
            src = convert(src, key)
        locations.append(src)
    advent.submit(1, min(locations))

    seed_ranges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    location_ranges = []
    for seed in seed_ranges:
        src_ranges = [seed]
        dst_ranges = []

        for key in MAPS.keys():
            for src, rng in src_ranges:
                dst_ranges.extend(convert_range(src, rng, key))
            src_ranges = [s for s in dst_ranges]
            dst_ranges = []
        location_ranges.extend(src_ranges)
    advent.submit(2, min([src for (src, _) in location_ranges]))


def read_puzzle(lines: list[str]) -> list[int]:
    # Read seed numbers
    seeds = lines[0]
    seeds = seeds[seeds.index(":") + 1 :].split(" ")
    seeds = [int(s.strip()) for s in seeds if s]

    # Read conversion maps
    key = None
    for line in lines[1:]:
        if "map" in line:
            key = line[: line.index("map") - 1]
        elif line:
            (dest, src, rng) = tuple(int(x) for x in line.strip().split(" "))
            MAPS[key][(src, rng)] = dest
    return seeds


def convert(src: int, key: str) -> int:
    """
    Convert src number using key's map.
    """
    for (src_start, rng), dest in MAPS[key].items():
        if src_start <= src <= src_start + rng:
            return dest + src - src_start
    return src


def convert_range(src: int, rng: int, key: str) -> list[tuple[int, int]]:
    """
    Convert a src range using key's map. Return a list of (start, range)
    tuples.

    Args:
        src (int): the input start
        rng (int): the input range
        key (str): the map's key

    Returns:
        list[tuple[int, int]]: a list of (start, range tuples)
    """
    out_ranges = []
    remaining = [(src, rng)]
    for (src_start, src_rng), dest in MAPS[key].items():
        rem = []
        for s0, r0 in remaining:
            inters, res = intersect(s0, r0, src_start, src_rng)
            if inters is not None:
                out_ranges.append(
                    (
                        dest + inters[0] - src_start,
                        inters[1],
                    )
                )
            for s, r in res:
                if r > 0:
                    rem.append((s, r))
        remaining = rem
    if remaining:
        out_ranges.extend(remaining)
    return out_ranges


def intersect(
    s0: int, r0: int, s1: int, r1: int
) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    """
    Find the intersection of two (start, range) intervals. Returns
    the intersection interval, as well as the remaining intervals outside
    of the intersection.

    Args:
        s0 (int): the input start
        r0 (int): the input range
        s1 (int): the intersect start
        r1 (int): the intersect range

    Returns:
        tuple[tuple[int, int], list[tuple[int, int]]]: the intersection interval,
        and the remainder of (s0, r0) - (s1, r1)
    """
    if s0 <= s1 <= s0 + r0:
        if s1 + r1 > s0 + r0:  # [s0  {s1    ]s0+r0   }s1+r1
            # return (intersection), [part of (s0, r0) not intersected]
            return (s1, s0 + r0 - s1), [(s0, s1 - s0)]
        else:  # [s0  {s1   }s1+r1   ]s0+r0
            return (s1, r1), [(s0, s1 - s0), (s1 + r1, s0 + r0 - s1 - r1)]
    if s1 <= s0 <= s1 + r1:
        if s1 + r1 >= s0 + r0:  # {s1 [s0    ]s0+r0 }s1+r1
            return (s0, r0), []
        else:  # {s1 [s0    }s1+r1   ]s0+r0
            return (s0, s1 + r1 - s0), [(s1 + r1, s0 + r0 - s1 - r1)]
    return None, [(s0, r0)]


if __name__ == "__main__":
    main()
