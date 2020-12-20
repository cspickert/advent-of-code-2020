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

    def part2(self, args):
        """
        Couldn't quite get this one on my own. Solution based on:
        https://gist.github.com/joshbduncan/65f810fe821c7a3ea81a1f5a444ea81e
        """
        _, bus_ids = args
        timestamp = 0
        step = 1
        offsets_and_bus_ids = [
            (offset, bus_id) for offset, bus_id in enumerate(bus_ids) if bus_id
        ]
        for offset, bus_id in offsets_and_bus_ids:
            while (timestamp + offset) % bus_id != 0:
                timestamp += step
            step *= bus_id
        return timestamp
