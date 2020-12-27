import math
from dataclasses import dataclass
from typing import Tuple

from base import BaseSolution


@dataclass(frozen=True)
class Tile:
    id: int
    edges: Tuple[str]
    rotation: int = 0
    flip: bool = False

    def __repr__(self):
        return f"Tile(id={self.id}, rot={self.rotation}, flip={self.flip})"

    @classmethod
    def parse(cls, text):
        lines = text.splitlines()
        tile_id = int(lines[0].rstrip(":").split()[-1])
        tile_data = lines[1:]
        return Tile(id=tile_id, edges=cls.make_edges(tile_data))

    @classmethod
    def make_edges(cls, tile_data):
        top = tile_data[0]
        left = "".join(row[0] for row in tile_data)
        bottom = tile_data[-1]
        right = "".join(row[-1] for row in tile_data)
        return (top, left, bottom, right)

    @property
    def rotated(self):
        edges = (
            self.edges[3],
            "".join(reversed(self.edges[0])),
            self.edges[1],
            "".join(reversed(self.edges[2])),
        )
        return Tile(id=self.id, edges=edges, rotation=(self.rotation + 1) % 4)

    @property
    def flipped(self):
        edges = (
            "".join(reversed(self.edges[0])),
            self.edges[3],
            "".join(reversed(self.edges[2])),
            self.edges[1],
        )
        return Tile(id=self.id, edges=edges, rotation=self.rotation, flip=not self.flip)

    @property
    def all_rotations(self):
        return [
            self,
            self.rotated,
            self.rotated.rotated,
            self.rotated.rotated.rotated,
        ]

    @property
    def all_orientations(self):
        return self.all_rotations + self.flipped.all_rotations


class Solution(BaseSolution):
    def load_data(self, input):
        blocks = input.split("\n\n")
        return [Tile.parse(block) for block in blocks]

    def part1(self, tiles):
        dim = int(math.sqrt(len(tiles)))
        grid = self.guess_solution(tiles=tiles, dim=dim, grid=[])
        assert grid
        return math.prod(
            tile.id
            for tile in (
                grid[self.grid_idx(0, 0, dim)],
                grid[self.grid_idx(0, dim - 1, dim)],
                grid[self.grid_idx(dim - 1, 0, dim)],
                grid[self.grid_idx(dim - 1, dim - 1, dim)],
            )
        )

    def guess_solution(self, tiles, dim, grid):
        for i in range(len(tiles)):
            for tile in tiles[i].all_orientations:
                result = self.check_solution(
                    tiles[:i] + tiles[i + 1 :], dim, grid + [tile]
                )
                if result is not None:
                    return result
        return None

    def check_solution(self, tiles, dim, grid):
        idx = len(grid) - 1
        row, col = self.grid_coords(idx, dim)
        if row > 0:
            up_idx = self.grid_idx(row - 1, col, dim)
            if grid[idx].edges[0] != grid[up_idx].edges[2]:
                return None
        if col > 0:
            lt_idx = self.grid_idx(row, col - 1, dim)
            if grid[idx].edges[1] != grid[lt_idx].edges[3]:
                return None
        if len(grid) == dim ** 2:
            return grid
        return self.guess_solution(tiles, dim, grid)

    def grid_coords(self, idx, dim):
        return idx // dim, idx % dim

    def grid_idx(self, row, col, dim):
        return dim * row + col


if __name__ == "__main__":
    from run import run

    run(["day20"])
