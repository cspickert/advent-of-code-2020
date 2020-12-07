from base import BaseSolution


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


class Solution(BaseSolution):
    def load_data(self, input):
        return input.splitlines()

    def part1(self, data):
        return max(get_seats(data))

    def part2(self, data):
        seats = sorted(get_seats(data))
        for i in range(1, len(seats)):
            if seats[i - 1] != seats[i] - 1:
                return seats[i] - 1
