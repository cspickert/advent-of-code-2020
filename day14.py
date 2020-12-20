import re
from dataclasses import dataclass, field
from typing import Dict, Literal

from base import BaseSolution


@dataclass
class State:
    version: Literal[1, 2] = 1
    mask: str = "X" * 36
    memory: Dict[int, int] = field(default_factory=dict)


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
        getattr(self, f"update_v{state.version}")(state)

    def update_v1(self, state):
        masked_value_str = self.apply_mask(self.value, state.mask, "X")
        state.memory[self.address] = int(masked_value_str, 2)

    def update_v2(self, state):
        masked_address_str = self.apply_mask(self.address, state.mask, "0")
        addresses = []
        stack = [masked_address_str]
        while stack:
            masked_address = stack.pop()
            try:
                index = masked_address.index("X")
                stack.extend(
                    masked_address[:index] + bit_char + masked_address[index + 1 :]
                    for bit_char in ("0", "1")
                )
            except ValueError:
                addresses.append(int(masked_address, 2))
        for address in addresses:
            state.memory[address] = self.value

    def apply_mask(self, value, mask, ignored_mask_chars):
        value_bits_str = bin(value)[2:].rjust(len(mask), "0")
        value_bits_str_masked = "".join(
            bit_char if mask_char in ignored_mask_chars else mask_char
            for bit_char, mask_char in zip(value_bits_str, mask)
        )
        return value_bits_str_masked


class Solution(BaseSolution):
    def load_data(self, input):
        return [Action.parse(line) for line in input.splitlines()]

    def part1(self, data):
        return self.process(data, version=1)

    def part2(self, data):
        return self.process(data, version=2)

    def process(self, data, version):
        state = State(version=version)
        for action in data:
            action.update(state)
        return sum(state.memory.values())
