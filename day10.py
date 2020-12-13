from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        data = [int(line) for line in input.splitlines()]
        return [0] + sorted(data) + [max(data) + 3]

    def part1(self, data):
        diffs = [0] * 4
        for i in range(1, len(data)):
            diffs[data[i] - data[i - 1]] += 1
        return diffs[1] * diffs[3]
