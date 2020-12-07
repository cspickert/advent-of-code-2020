from dataclasses import dataclass

from base import BaseSolution


class Entry:
    def __init__(self, line):
        pieces = line.split()
        self.low, self.high = (int(c) for c in pieces[0].split("-"))
        self.char = pieces[1][0]
        self.password = pieces[-1]


class Solution(BaseSolution):
    def load_data(self, input):
        return [Entry(line) for line in input.splitlines()]

    def part1(self, entries):
        def validate(entry):
            count = sum(1 if c == entry.char else 0 for c in entry.password)
            return count >= entry.low and count <= entry.high

        return sum(validate(entry) for entry in entries)

    def part2(self, entries):
        def validate(entry):
            pos1_match = entry.password[entry.low - 1] == entry.char
            pos2_match = entry.password[entry.high - 1] == entry.char
            return pos1_match != pos2_match

        return sum(validate(entry) for entry in entries)
