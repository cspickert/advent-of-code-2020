def part1(data):
    total = 0
    for group in data:
        answers = set()
        for item in group:
            answers.update(item)
        total += len(answers)
    print(total)


def part2(data):
    total = 0
    for group in data:
        answers = set(group[0])
        for item in group[1:]:
            answers.intersection_update(item)
        total += len(answers)
    print(total)


if __name__ == "__main__":
    from input import day06

    data = [group.split() for group in day06.split("\n\n")]
    part1(data)
    part2(data)
