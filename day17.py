from base import BaseSolution


ADJ_OFFSETS = {
    (x, y, z)
    for x in range(-1, 2)
    for y in range(-1, 2)
    for z in range(-1, 2)
    if any((x, y, z))
}


class Solution(BaseSolution):
    def load_data(self, input):
        return {
            (x, y, 0)
            for y, row in enumerate(input.splitlines())
            for x, cube in enumerate(row)
            if cube == "#"
        }

    def part1(self, state):
        for _ in range(6):
            state = self.get_next_state(state)
        return len(state)

    def get_next_state(self, state):
        new_state = set()
        for coords in self.get_all_coords(state):
            active_neighbors = sum(
                adj_coords in state for adj_coords in self.get_adj_coords(*coords)
            )
            if coords in state:
                if active_neighbors == 2 or active_neighbors == 3:
                    new_state.add(coords)
            else:
                if active_neighbors == 3:
                    new_state.add(coords)
        return new_state

    def get_all_coords(self, state):
        all_coords = set(state)
        for coords in state:
            all_coords.update(self.get_adj_coords(*coords))
        return all_coords

    def get_adj_coords(self, x, y, z):
        return {(x + dx, y + dy, z + dz) for dx, dy, dz in ADJ_OFFSETS}
