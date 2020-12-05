import re


def validate_int(value, value_min=None, value_max=None):
    try:
        value = int(value)
    except ValueError:
        return False
    if value_min is not None and value < value_min:
        return False
    if value_max is not None and value > value_max:
        return False
    return True


def validate_year(year_min, year_max):
    def validate(value):
        return len(value) == 4 and validate_int(value, year_min, year_max)

    return validate


def validate_height():
    def validate(value):
        if value.endswith("cm"):
            value_min, value_max = 150, 193
        elif value.endswith("in"):
            value_min, value_max = 59, 76
        else:
            return False
        return validate_int(value[:-2], value_min, value_max)

    return validate


def validate_hex_color():
    def validate(value):
        return bool(re.match(r"#[0-9a-f]{6}", value))

    return validate


def validate_eye_color():
    def validate(value):
        return value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    return validate


def validate_digits(digits):
    def validate(value):
        return len(value) == digits and validate_int(value)

    return validate


required_fields = {
    "byr": validate_year(1920, 2002),
    "iyr": validate_year(2010, 2020),
    "eyr": validate_year(2020, 2030),
    "hgt": validate_height(),
    "hcl": validate_hex_color(),
    "ecl": validate_eye_color(),
    "pid": validate_digits(9),
    # "cid",
}


def has_required_fields(record):
    return all(field in record for field in required_fields)


def part1(data):
    count = sum(has_required_fields(record) for record in data)
    print(count)


def part2(data):
    count = 0
    for record in data:
        valid_record = dict(record)
        for field in record:
            value = record[field]
            validate = required_fields.get(field, lambda _: True)
            if not validate(value):
                valid_record.pop(field)
        if has_required_fields(valid_record):
            count += 1
    print(count)


if __name__ == "__main__":
    from input import day04

    data = [
        dict(pair.split(":") for pair in section.split())
        for section in day04.split("\n\n")
    ]
    part1(data)
    part2(data)
