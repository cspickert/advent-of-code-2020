import re
from dataclasses import dataclass, field
from typing import List

from base import BaseSolution


@dataclass
class State:
    mask: str = "X" * 36
    memory: List[int] = field(default_factory=lambda: [0] * 128000)


class Action:
    @classmethod
    def parse(cls, line):
        return next(
            subcls(match)
            for subcls in cls.__subclasses__()
            if (match := subcls.pattern.match(line))
        )

    def update(self, state):
        pass


class SetMask(Action):
    pattern = re.compile(r"^mask = ([01X]+)$")

    def __init__(self, match):
        self.value = match.group(1)

    def __repr__(self):
        return f"SetMask({self.value})"

    def update(self, state):
        state.mask = self.value


class SetMemory(Action):
    pattern = re.compile(r"^mem\[(\d+)\] = (\d+)$")

    def __init__(self, match):
        self.address = int(match.group(1))
        self.value = int(match.group(2))

    def __repr__(self):
        return f"SetMemory({self.address}, {self.value})"

    def update(self, state):
        value_bits_str = bin(self.value)[2:].rjust(len(state.mask), "0")
        value_bits_str_masked = "".join(
            bit_char if mask_char == "X" else mask_char
            for bit_char, mask_char in zip(value_bits_str, state.mask)
        )
        state.memory[self.address] = int(value_bits_str_masked, 2)


class Solution(BaseSolution):
    def load_data(self, input):
        return [Action.parse(line) for line in input.splitlines()]

    def part1(self, data):
        state = State()
        for action in data:
            action.update(state)
        return sum(state.memory)


if __name__ == "__main__":
    from run import run

    run(["day14"])
