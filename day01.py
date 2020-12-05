def part1(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print(nums[i] * nums[j])
                return


def part2(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print(nums[i] * nums[j] * nums[k])
                    return


if __name__ == "__main__":
    from input import day01

    nums = [int(line) for line in day01.split()]
    part1(nums)
    part2(nums)
