from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        self.data = [int(i) for i in input.split(",")]

    def part1(self, *args):
        for i, num in enumerate(self.generate_turns(), 1):
            if i == 2020:
                return num

    def part2(self, *args):
        for i, num in enumerate(self.generate_turns(), 1):
            if i == 30000000:
                return num

    def generate_turns(self):
        for num in self.data:
            yield num
        seen = {num: turn for turn, num in enumerate(self.data)}
        turn = len(self.data) - 1
        last_num = self.data[turn]
        while True:
            next_num = turn - seen[last_num] if last_num in seen else 0
            yield next_num
            seen[last_num] = turn
            last_num = next_num
            turn += 1
