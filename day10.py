from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        data = [int(line) for line in input.splitlines()]
        return [0, *sorted(data), max(data) + 3]

    def part1(self, data):
        diffs = [0] * 4
        for i in range(1, len(data)):
            diffs[data[i] - data[i - 1]] += 1
        return diffs[1] * diffs[3]

    def part2(self, data):
        counts = {}
        return self.do_part2(data, counts)

    def do_part2(self, data, counts):
        if len(data) == 1:
            return 1
        num, *rest = data
        if num in counts:
            return counts[num]
        result = 0
        for i in range(len(rest)):
            if rest[i] - num > 3:
                break
            result += self.do_part2(rest[i:], counts)
        counts[num] = result
        return result
