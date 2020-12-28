import math

from base import BaseSolution


class Node:
    @classmethod
    def from_list(cls, numbers):
        head = None
        prev = None
        for num in numbers:
            node = Node(num)
            if not head:
                head = node
            if prev:
                prev.next = node
            prev = node
        prev.next = head
        return head

    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f"Node({self.value})"

    def __iter__(self):
        yield self
        current = self.next
        while current and current != self:
            yield current
            current = current.next

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, Node):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.value < other.value
        return self.value < other

    def __ge__(self, other):
        if isinstance(other, Node):
            return self.value >= other.value
        return self.value >= other

    def find(self, value):
        return next(n for n in self if n.value == value)


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(i) for i in input]

    def part1(self, data):
        node = Node.from_list(data)
        node_min = min(node)
        node_max = max(node)
        mapping = {n.value: n for n in node}
        for i in range(1, 101):
            # print("--", "move", i, "--")
            node = self.do_move(node, node_min, node_max, mapping)
            # print()
        while node.value != 1:
            node = node.next
        return "".join(str(i.value) for i in list(node)[1:])

    def part2(self, orig_data):
        data = orig_data + [i for i in range(max(orig_data) + 1, 1000001)]
        node = Node.from_list(data)
        node_min = min(node)
        node_max = max(node)
        mapping = {n.value: n for n in node}
        for i in range(10000000):
            node = self.do_move(node, node_min, node_max, mapping)
        while node.value != 1:
            node = node.next
        return math.prod(n.value for n in list(node)[1:3])

    def do_move(self, current, node_min, node_max, mapping):
        # print(
        #     "cups:",
        #     " ".join(f"({i.value})" if i is current else str(i.value) for i in current),
        # )

        removed_head = current.next
        rest = removed_head
        removed_tail = rest
        for _ in range(3):
            removed_tail = rest
            rest = rest.next
        current.next = rest
        removed_tail.next = None

        # print("pick up:", ", ".join(str(i.value) for i in removed_head))

        # Find the destination cup.
        dest_cup_label = current.value - 1
        while dest_cup_label not in mapping or mapping[dest_cup_label] in removed_head:
            if dest_cup_label < node_min.value:
                dest_cup_label = node_max.value
            else:
                dest_cup_label -= 1
        dest_cup_node = mapping[dest_cup_label]

        # print("destination:", dest_cup_label)

        # Update the current cup.
        current = current.next

        # Add the removed cups.
        dest_cup_tail = dest_cup_node.next
        dest_cup_node.next = removed_head
        removed_tail.next = dest_cup_tail

        # Return the current node.
        return current
