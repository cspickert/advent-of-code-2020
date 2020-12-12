from itertools import combinations

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(line) for line in input.splitlines()]

    def part1(self, data):
        for i in range(25, len(data)):
            if not any(
                sum(pair) == data[i] for pair in combinations(data[i - 25 : i], 2)
            ):
                return data[i]
        return None

    def part2(self, data):
        target = self.part1(data)
        for size in range(2, len(data)):
            for i in range(size, len(data)):
                span = data[i - size : i]
                if sum(span) == target:
                    return min(span) + max(span)
        return None
