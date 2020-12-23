from base import BaseSolution


ADJ_OFFSETS = {
    (x, y, z, w)
    for x in range(-1, 2)
    for y in range(-1, 2)
    for z in range(-1, 2)
    for w in range(-1, 2)
    if any((x, y, z, w))
}


class Solution(BaseSolution):
    def load_data(self, input):
        return {
            (x, y, 0, 0)
            for y, row in enumerate(input.splitlines())
            for x, cube in enumerate(row)
            if cube == "#"
        }

    def part1(self, state):
        return self.get_result(state, 3)

    def part2(self, state):
        return self.get_result(state, 4)

    def get_result(self, state, dims):
        for _ in range(6):
            state = self.get_next_state(state, dims)
        return len(state)

    def get_next_state(self, state, dims):
        new_state = set()
        for coords in self.get_all_coords(state, dims):
            active_neighbors = sum(
                adj_coords in state for adj_coords in self.get_adj_coords(coords, dims)
            )
            if coords in state:
                if active_neighbors in (2, 3):
                    new_state.add(coords)
            elif active_neighbors == 3:
                new_state.add(coords)
        return new_state

    def get_all_coords(self, state, dims):
        all_coords = set(state)
        for coords in state:
            all_coords.update(self.get_adj_coords(coords, dims))
        return all_coords

    def get_adj_coords(self, coords, dims):
        assert 3 <= dims <= 4
        x, y, z, w = coords
        return {
            (x + dx, y + dy, z + dz, w + dw)
            for dx, dy, dz, dw in {
                offset for offset in ADJ_OFFSETS if not any(offset[dims:])
            }
        }
