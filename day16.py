import math
from dataclasses import dataclass
from typing import List

from base import BaseSolution


@dataclass
class Field:
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

    def validate(self, fields):
        return not any(self.invalid_values(fields))

    def valid_fields(self, fields):
        return [
            {field.name for field in fields if field.validate(value)}
            for value in self.values
        ]

    def invalid_values(self, fields):
        for value in self.values:
            if not any(field.validate(value) for field in fields):
                yield value


class Solution(BaseSolution):
    def load_data(self, input):
        blocks = input.split("\n\n")
        fields = [Field.parse(line) for line in blocks[0].splitlines()]
        ticket = Ticket.parse(blocks[1].splitlines()[1])
        nearby_tickets = [Ticket.parse(line) for line in blocks[2].splitlines()[1:]]
        return (fields, ticket, nearby_tickets)

    def part1(self, data):
        fields, _, nearby_tickets = data
        return sum(sum(ticket.invalid_values(fields)) for ticket in nearby_tickets)

    def part2(self, data):
        fields, ticket, nearby_tickets = data

        # Get the list of tickets whose values are all valid.
        valid_nearby_tickets = [
            ticket for ticket in nearby_tickets if ticket.validate(fields)
        ]

        # For each ticket, create a set of possible fields for each
        # value on the ticket.
        all_possible_fields = [
            ticket.valid_fields(fields) for ticket in valid_nearby_tickets
        ]

        # Create a list containing sets of possible fields for each
        # value index on a ticket by intersecting the valid set of
        # fields for each ticket at each value index.
        result = []
        for field_index in range(len(ticket.values)):
            possible_fields = all_possible_fields[0][field_index]
            for ticket_index in range(1, len(all_possible_fields)):
                next_possible_fields = (
                    possible_fields & all_possible_fields[ticket_index][field_index]
                )
                if next_possible_fields:
                    # NOTE: I ran into a case where this loop produced
                    # an empty set of possible fields at index 1 for the
                    # problem input, hence this check.
                    possible_fields = next_possible_fields
            result.insert(field_index, possible_fields)

        # Repeatedly iterate over the list. Look for sets containing one
        # possible field and remove that field from the other sets.
        while True:
            done = True
            updated = False
            for index in range(len(result)):
                if len(result[index]) == 1:
                    for other_index in range(len(result)):
                        if index != other_index:
                            result[other_index] -= result[index]
                            updated = True
                else:
                    done = False
            if done:
                break
            elif not updated:
                # If no updates occurred during an iteration, avoid
                # looping infinitely.
                raise Exception("Unable to solve.")

        # Flatten the list of confirmed field names.
        confirmed_fields = [fields.pop() for fields in result]

        # Multiply ticket values for fields whose names start with
        # "departure".
        return math.prod(
            ticket.values[i]
            for i, field in enumerate(confirmed_fields)
            if field.startswith("departure")
        )
