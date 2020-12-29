from base import BaseSolution


def transform(loop_size, subject_number):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


def find_loop_size(public_key, subject_number):
    value = 1
    loop_size = 0
    while True:
        if value == public_key:
            return loop_size
        value *= subject_number
        value %= 20201227
        loop_size += 1


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(line) for line in input.splitlines()]

    def part1(self, data):
        card_public_key, door_public_key = data
        card_loop_size = find_loop_size(card_public_key, 7)
        door_loop_size = find_loop_size(door_public_key, 7)
        card_encryption_key = transform(card_loop_size, door_public_key)
        door_encryption_key = transform(door_loop_size, card_public_key)
        assert card_encryption_key == door_encryption_key
        return card_encryption_key

