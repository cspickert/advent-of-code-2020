def make_get_value(low_char, high_char, low_val, high_val):
    def get_value(seq):
        low, high = low_val, high_val
        for char in seq:
            if char == low_char:
                high = (low + high) // 2
            if char == high_char:
                low = (low + high) // 2 + 1
        assert low == high
        return low

    return get_value


get_row = make_get_value("F", "B", 0, 127)
get_col = make_get_value("L", "R", 0, 7)


def get_seats(data):
    seats = []
    for sequence in data:
        row, col = get_row(sequence), get_col(sequence)
        seats.append(row * 8 + col)
    return seats


def part1(data):
    print(max(get_seats(data)))


def part2(data):
    seats = sorted(get_seats(data))
    for i in range(1, len(seats)):
        if seats[i - 1] != seats[i] - 1:
            print(seats[i] - 1)
            return


if __name__ == "__main__":
    from input import day05

    data = day05.splitlines()
    part1(data)
    part2(data)
