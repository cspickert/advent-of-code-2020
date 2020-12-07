import math

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return input.splitlines()

    def part1(self, data):
        return self.count_trees(data, 3, 1)

    def part2(self, data):
        return math.prod(
            self.count_trees(data, dx, dy)
            for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2),)
        )

    def count_trees(self, data, dx, dy):
        return sum(
            1 if data[y][y // dy * dx % len(data[y])] == "#" else 0
            for y in range(0, len(data), dy)
        )
