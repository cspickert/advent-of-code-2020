from base import BaseSolution


def build_validate(lines):
    rules = {
        int(rule_id): [
            [int(i) if i.isdigit() else eval(i) for i in alls.split()]
            for alls in anys.split(" | ")
        ]
        for rule_id, anys in dict(line.split(": ", 1) for line in lines).items()
    }

    def expand(rule_id):
        if rule_id not in rules:
            return {rule_id}
        results = set()
        for sequence in rules[rule_id]:
            seq_exp_1 = expand(sequence[0])
            if len(sequence) == 1:
                results.update(seq_exp_1)
            elif len(sequence) == 2:
                seq_exp_2 = expand(sequence[1])
                for i in seq_exp_1:
                    for j in seq_exp_2:
                        results.add(i + j)
        return results

    all_possible_messages = expand(0)

    def validate(message):
        return message in all_possible_messages

    return validate


class Solution(BaseSolution):
    def load_data(self, input):
        blocks = input.split("\n\n")
        validate = build_validate(blocks[0].splitlines())
        return validate, blocks[1].splitlines()

    def part1(self, args):
        validate, messages = args
        return sum(validate(message) for message in messages)
