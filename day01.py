def day01_01(f):
    nums = [int(line) for line in f]
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print(nums[i] * nums[j])
                return


def day01_02(f):
    nums = [int(line) for line in f]
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print(nums[i] * nums[j] * nums[k])
                    return


if __name__ == "__main__":
    for fn in [day01_01, day01_02]:
        with open("input/day01.txt") as f:
            fn(f)
