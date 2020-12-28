from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(i) for i in input]

    def part1(self, data):
        current_idx = 0
        for i in range(1, 101):
            data, current_idx = self.do_move(data, current_idx)
        idx = data.index(1)
        return "".join(str(i) for i in data[idx + 1 :] + data[:idx])

    def do_move(self, data, current_idx=0):
        current_label = data[current_idx]

        # Remove the 3 cups clockwise from the current cup.
        removal_indices = []
        removal_idx = current_idx + 1
        while len(removal_indices) < 3:
            removal_idx %= len(data)
            removal_indices.append(removal_idx)
            removal_idx += 1

        removed = [data[i] for i in removal_indices]
        data = [data[i] for i in range(len(data)) if i not in removal_indices]

        # Find the destination cup.
        dest_cup_label = current_label - 1
        while dest_cup_label not in data:
            if dest_cup_label < min(data):
                dest_cup_label = max(data)
                break
            dest_cup_label -= 1
        dest_cup_idx = data.index(dest_cup_label)

        # Update the current cup.
        current_label = data[(data.index(current_label) + 1) % len(data)]

        # Add the removed cups.
        insertion_idx = dest_cup_idx + 1
        data = data[:insertion_idx] + removed + data[insertion_idx:]

        # Get the index of the current cup.
        current_idx = data.index(current_label)

        # Return the result.
        return data, current_idx
