from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [group.split() for group in input.split("\n\n")]

    def part1(self, data):
        total = 0
        for group in data:
            answers = set()
            for item in group:
                answers.update(item)
            total += len(answers)
        return total

    def part2(self, data):
        total = 0
        for group in data:
            answers = set(group[0])
            for item in group[1:]:
                answers.intersection_update(item)
            total += len(answers)
        return total
