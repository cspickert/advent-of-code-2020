import math


def count_trees(data, dx, dy):
    return sum(
        1 if data[y][y // dy * dx % len(data[y])] == "#" else 0
        for y in range(0, len(data), dy)
    )


def part1(data):
    count = count_trees(data, 3, 1)
    print(count)


def part2(data):
    result = math.prod(
        count_trees(data, dx, dy)
        for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2),)
    )
    print(result)


if __name__ == "__main__":
    from input import day03

    data = [line for line in day03.splitlines()]
    part1(data)
    part2(data)
