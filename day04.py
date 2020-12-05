required_fields = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    # "cid",
}


def part1(data):
    count = sum(
        1 if all(field in record for field in required_fields) else 0 for record in data
    )
    print(count)


if __name__ == "__main__":
    from input import day04

    data = [
        dict(pair.split(":") for pair in section.split())
        for section in day04.split("\n\n")
    ]
    part1(data)
