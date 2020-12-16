import math

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        lines = input.splitlines()
        return (
            int(lines[0]),
            [int(i) if i.isdigit() else 0 for i in lines[1].split(",")],
        )

    def part1(self, args):
        timestamp, bus_ids = args
        bus_id, bus_timestamp = min(
            (
                (bus_id, math.ceil(timestamp / bus_id) * bus_id)
                for bus_id in filter(None, bus_ids)
            ),
            key=lambda pair: pair[1],
        )
        return bus_id * (bus_timestamp - timestamp)
