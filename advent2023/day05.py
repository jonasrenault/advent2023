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


if __name__ == "__main__":
    main()
