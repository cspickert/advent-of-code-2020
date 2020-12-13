from functools import cached_property, lru_cache
from itertools import combinations
from typing import Callable, List, Optional, Tuple

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input: str) -> List[List[str]]:
        return [list(line) for line in input.splitlines()]

    def part1(self, grid: List[List[str]]) -> int:
        self.grid = grid
        return self.solve(self.count_adj_occupied, 4)

    def part2(self, grid: List[List[str]]) -> int:
        self.grid = grid
        return self.solve(self.count_visible_occupied, 5)

    def solve(
        self, count_occupied_from: Callable[[int, int], int], threshold: int
    ) -> int:
        while True:
            changed = self.do_round(count_occupied_from, threshold)
            if not changed:
                break
        return self.count_all_occupied()

    def do_round(
        self, count_occupied_from: Callable[[int, int], int], threshold: int
    ) -> bool:
        next_grid = [row[:] for row in self.grid]
        changed = False
        for row, col in self.all_coords:
            num_occupied = count_occupied_from(row, col)
            if self.grid[row][col] == "L" and not num_occupied:
                next_grid[row][col] = "#"
                changed = True
            elif self.grid[row][col] == "#" and num_occupied >= threshold:
                next_grid[row][col] = "L"
                changed = True
        self.grid = next_grid
        return changed

    @cached_property
    def all_coords(self) -> List[Tuple[int, int]]:
        return [
            (row, col)
            for row in range(len(self.grid))
            for col in range(len(self.grid[row]))
        ]

    def count_all_occupied(self) -> int:
        return sum(self.grid[row][col] == "#" for row, col in self.all_coords)

    def count_adj_occupied(self, row: int, col: int) -> int:
        return sum(
            self.grid[adj_row][adj_col] == "#"
            for adj_row, adj_col in self.adj_coords(row, col)
        )

    def count_visible_occupied(self, row: int, col: int) -> int:
        return sum(
            self.grid[seat_row][seat_col] == "#"
            for seat_row, seat_col in self.visible_seat_coords(row, col)
        )

    @lru_cache
    def visible_seat_coords(self, row: int, col: int) -> List[Tuple[int, int]]:
        result = []
        for offset in self.adj_offsets:
            visible_seat = self.visible_seat_at_offset(row, col, offset)
            if visible_seat:
                result.append(visible_seat)
        return result

    def visible_seat_at_offset(
        self, row: int, col: int, offset: Optional[Tuple[int, int]]
    ) -> Optional[Tuple[int, int]]:
        if not offset:
            return None
        dr, dc = offset
        while True:
            row += dr
            col += dc
            if not self.is_valid_coord(row, col):
                break
            if self.grid[row][col] in ("L", "#"):
                return row, col
        return None

    @lru_cache
    def adj_coords(self, row: int, col: int) -> List[Tuple[int, int]]:
        result = []
        for dr, dc in self.adj_offsets:
            adj_row = row + dr
            adj_col = col + dc
            if self.is_valid_coord(adj_row, adj_col):
                result.append((adj_row, adj_col))
        return result

    def is_valid_coord(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])

    @cached_property
    def adj_offsets(self) -> List[Tuple[int, int]]:
        return [
            (dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)
        ]
