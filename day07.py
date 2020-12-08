from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        data = {}
        for line in input.splitlines():
            parent, rest = line.split("contain")
            parent = " ".join(parent.split()[:-1])
            children = rest.split(",")
            for i, child in enumerate(children):
                child = " ".join(child.split()[:-1])
                if child == "no other":
                    children = []
                    break
                count, child = child.split(" ", 1)
                count = int(count)
                children[i] = (count, child)
            data[parent] = children
        return data

    def contains(self, data, parent, child):
        for _, contained in data[parent]:
            if child == contained or self.contains(data, contained, child):
                return True
        return False

    def count_contained(self, data, parent):
        total = 0
        for count, contained in data[parent]:
            total += count
            total += count * self.count_contained(data, contained)
        return total

    def part1(self, data):
        return sum(self.contains(data, parent, "shiny gold") for parent in data)

    def part2(self, data):
        return self.count_contained(data, "shiny gold")
