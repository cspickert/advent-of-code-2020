from functools import lru_cache

from base import BaseSolution


# Offsets based on diagram here:
# https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0405/MARTIN/Hex.pdf
DIRECTIONS = {
    "ne": (0, 1, 1),
    "nw": (-1, 0, 1),
    "se": (1, 0, -1),
    "sw": (0, -1, -1),
    "e": (1, 1, 0),
    "w": (-1, -1, 0),
}


def parse_line(line):
    while line:
        for direction in DIRECTIONS:
            if line.startswith(direction):
                yield direction
                line = line[len(direction) :]


class Solution(BaseSolution):
    def load_data(self, input):
        return [list(parse_line(line)) for line in input.splitlines()]

    def part1(self, data):
        tiles = self.get_tiles(data)
        return sum(tiles.values())

    def part2(self, data):
        tiles = self.get_tiles(data)
        for _ in range(100):
            updated_tiles = {}
            for position in self.get_all_positions(tiles):
                if self.get_next_tile(tiles, position):
                    updated_tiles[position] = True
            tiles = updated_tiles
        return sum(tiles.values())

    def get_tiles(self, data):
        tiles = {}
        for path in data:
            position = (0, 0, 0)
            for direction in path:
                position = self.get_adj_position(position, direction)
            tiles[position] = not tiles.get(position, False)
        return tiles

    def get_next_tile(self, tiles, position):
        count = sum(self.get_adj_tiles(tiles, position).values())
        if tiles.get(position, False):
            if count == 0 or count > 2:
                return False
            return True
        return count == 2

    def get_adj_tiles(self, tiles, position):
        return {
            adj_position: tiles.get(adj_position, False)
            for adj_position in (
                self.get_adj_position(position, direction) for direction in DIRECTIONS
            )
        }

    @lru_cache
    def get_adj_position(self, position, direction):
        x, y, z = position
        dx, dy, dz = DIRECTIONS[direction]
        return (x + dx, y + dy, z + dz)

    def get_all_positions(self, tiles):
        return set(tiles.keys()) | {
            self.get_adj_position(position, direction)
            for direction in DIRECTIONS
            for position in tiles
        }
