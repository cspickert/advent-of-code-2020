from dataclasses import dataclass
from typing import List

from base import BaseSolution


@dataclass
class Constraint:
    name: str
    ranges: List[range]

    @classmethod
    def parse(cls, line):
        name, rest = line.split(": ")
        rest = [tuple(int(i) for i in pair.split("-")) for pair in rest.split(" or ")]
        ranges = [range(pair[0], pair[1] + 1) for pair in rest]
        return cls(name, ranges)

    def validate(self, value):
        return any(value in r for r in self.ranges)


@dataclass
class Ticket:
    values: List[int]

    @classmethod
    def parse(cls, line):
        return cls(values=[int(i) for i in line.split(",")])

    def invalid_values(self, constraints):
        for value in self.values:
            if not any(constraint.validate(value) for constraint in constraints):
                yield value


class Solution(BaseSolution):
    def load_data(self, input):
        blocks = input.split("\n\n")
        constraints = [Constraint.parse(line) for line in blocks[0].splitlines()]
        ticket = Ticket.parse(blocks[1].splitlines()[1])
        nearby_tickets = [Ticket.parse(line) for line in blocks[2].splitlines()[1:]]
        return (constraints, ticket, nearby_tickets)

    def part1(self, data):
        constraints, _, nearby_tickets = data
        return sum(sum(ticket.invalid_values(constraints)) for ticket in nearby_tickets)
