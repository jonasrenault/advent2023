from utils.utils import Advent

advent = Advent(11)


def main():
    lines = advent.get_input_lines()
    grid = expand(lines)
    galaxies = find_galaxies(grid)

    distances = 0
    for idx, (sr, sc) in enumerate(galaxies):
        for dr, dc in galaxies[idx + 1 :]:
            d = abs(sr - dr) + abs(sc - dc)
            distances += d

    advent.submit(1, distances)

    grid = advent.get_input_lines()
    galaxies = find_galaxies(grid)
    er, ec = get_empty_rows_cols(grid)
    factor = 1000000 - 1
    distances = 0
    for idx, (sr, sc) in enumerate(galaxies):
        for dr, dc in galaxies[idx + 1 :]:
            d = abs(sr - dr) + abs(sc - dc)
            d += factor * count_empty(er, ec, (sr, sc), (dr, dc))
            distances += d

    advent.submit(2, distances)


def count_empty(
    er: list[int], ec: list[int], src: tuple[int, int], dst: tuple[int, int]
) -> int:
    """
    Count the number of empty rows anc columns between the src node and the dest node.

    Args:
        er (list[int]): list of empty rows
        ec (list[int]): list of empty columns
        src (tuple[int, int]): source node coordinates
        dst (tuple[int, int]): dest node coordinates

    Returns:
        int: the number of empty rows or cols between src and dest
    """
    ar, br = min(src[0], dst[0]), max(src[0], dst[0])
    ac, bc = min(src[1], dst[1]), max(src[1], dst[1])
    cr = sum([1 for r in er if ar <= r <= br])
    cc = sum([1 for c in ec if ac <= c <= bc])
    return cr + cc


def find_galaxies(grid: list[str]) -> list[tuple[int, int]]:
    """
    Find coordinates for galaxies

    Args:
        grid (list[str]): the grid

    Returns:
        list[tuple[int, int]]: the galaxies' coordinates
    """
    galaxies = []
    for x, row in enumerate(grid):
        for y, c in enumerate(row):
            if c != ".":
                galaxies.append((x, y))
    return galaxies


def get_empty_rows_cols(grid: list[str]) -> tuple[list[int]]:
    """
    Get the indices for empty rows and cols

    Args:
        grid (list[str]): the grid

    Returns:
        tuple[list[int]]: list of empty rows and cols
    """
    rows = list()
    cols = set()
    for r, row in enumerate(grid):
        if "#" not in row:
            rows.append(r)
        for c, ch in enumerate(row):
            if ch == "#":
                cols.add(c)

    return rows, [c for c in range(len(grid[0])) if c not in cols]


def expand(grid: list[str]) -> list[str]:
    """
    Double each empty row and col in the grid

    Args:
        grid (list[str]): the grid

    Returns:
        list[str]: the expanded grid
    """
    # find empty rows and cols
    rows, cols = get_empty_rows_cols(grid)

    # add new columns
    new_grid = []
    for row in grid:
        new_row = row
        for idx, c in enumerate(cols):
            new_row = new_row[: c + idx] + "." + row[c:]
        new_grid.append(new_row)

    # add new rows
    l = len(new_grid[0])
    for i, r in enumerate(rows):
        new_grid.insert(r + i, "." * l)

    return new_grid


if __name__ == "__main__":
    main()
