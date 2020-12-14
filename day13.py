import math

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        lines = input.splitlines()
        return (int(lines[0]), sorted(int(i) for i in lines[1].split(",") if i != "x"))

    def part1(self, args):
        timestamp, bus_ids = args
        bus_id, bus_timestamp = min(
            ((bus_id, math.ceil(timestamp / bus_id) * bus_id) for bus_id in bus_ids),
            key=lambda pair: pair[1],
        )
        return bus_id * (bus_timestamp - timestamp)
