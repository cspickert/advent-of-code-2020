from dataclasses import dataclass


class Entry:
    def __init__(self, line):
        pieces = line.split()
        self.low, self.high = (int(c) for c in pieces[0].split("-"))
        self.char = pieces[1][0]
        self.password = pieces[-1]


def part1(entry):
    count = sum(1 if c == entry.char else 0 for c in entry.password)
    return count >= entry.low and count <= entry.high


def part2(entry):
    pos1_match = entry.password[entry.low - 1] == entry.char
    pos2_match = entry.password[entry.high - 1] == entry.char
    return pos1_match != pos2_match


def run(validate, entries):
    valid_count = sum(1 if validate(entry) else 0 for entry in entries)
    print(valid_count)


if __name__ == "__main__":
    from input import day02

    entries = [Entry(line) for line in day02.splitlines()]
    run(part1, entries)
    run(part2, entries)
