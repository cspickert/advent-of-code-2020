from base import BaseSolution


class History:
    def __init__(self):
        self.history = set()

    def __contains__(self, data):
        return self.serialize(data) in self.history

    def add(self, data):
        self.history.add(self.serialize(data))

    def serialize(self, data):
        return tuple("".join(str(i) for i in deck) for deck in data)


class Solution(BaseSolution):
    def load_data(self, input):
        return tuple(
            [int(line) for line in block.splitlines()[1:]]
            for block in input.split("\n\n")
        )

    def part1(self, data):
        data = self.do_game(data)
        return self.count_score(data)

    def part2(self, data):
        data = self.do_game(data, recursive=True)
        return self.count_score(data)

    def count_score(self, data):
        return sum(
            i * card for i, card in enumerate(reversed(data[0] or data[1]), start=1)
        )

    def do_game(self, data, recursive=False):
        history = History()
        while all(data):
            if data in history:
                return (data[0] + data[1], [])
            history.add(data)
            data = self.do_round(data, recursive=recursive)
        return data

    def do_round(self, data, recursive=False):
        (card1, *deck1), (card2, *deck2) = data

        winner = None
        if recursive and len(deck1) >= card1 and len(deck2) >= card2:
            sub_data = self.do_game((deck1[:card1], deck2[:card2]), recursive=recursive)
            if sub_data[0]:
                winner = 0
            if sub_data[1]:
                winner = 1
        elif card1 > card2:
            winner = 0
        elif card2 > card1:
            winner = 1

        if winner == 0:
            return ([*deck1, card1, card2], deck2)
        elif winner == 1:
            return (deck1, [*deck2, card2, card1])
        else:
            assert False, "no winner"
