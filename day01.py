from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(line) for line in input.splitlines()]

    def part1(self, nums):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == 2020:
                    return nums[i] * nums[j]

    def part2(self, nums):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 2020:
                        return nums[i] * nums[j] * nums[k]
