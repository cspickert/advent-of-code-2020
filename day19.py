from collections import defaultdict

from base import BaseSolution


"""
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab, aba

validate(aab, 0) ->
    any(
        validate(a, 1) and validate(ab, 2),
        validate(aa, 1) and validate(b, 2)
    )

validate(a, 1) ->
    a == a

validate(ab, 2) ->
    any(
        any((validate(a, 1) and validate(b, 3)),),
        any((validate(a, 3) and validate(b, 1)),),
    )

validate(b, 3) ->
    b == b
"""


def parse_rules(lines):
    return {
        int(rule_id): [
            [int(i) if i.isdigit() else eval(i) for i in alls.split()]
            for alls in anys.split(" | ")
        ]
        for rule_id, anys in dict(line.split(": ", 1) for line in lines).items()
    }


def build_validate(rules):
    cache = defaultdict(dict)

    def cached(fn):
        def wrapper(message, rule_id=0):
            if message in cache[rule_id]:
                return cache[rule_id][message]
            result = fn(message, rule_id)
            cache[rule_id][message] = result
            return result

        return wrapper

    def validate_seq(message, seq):
        first, *rest = seq
        if not rest:
            return validate(message, first)
        for i in range(len(message) - 1, 0, -1):
            if validate(message[:i], first) and validate_seq(message[i:], rest):
                return True
        return False

    @cached
    def validate(message, rule_id=0):
        if rule_id not in rules:
            return message == rule_id
        return any(validate_seq(message, seq) for seq in rules[rule_id])

    return validate


class Solution(BaseSolution):
    def load_data(self, input):
        blocks = input.split("\n\n")
        rules = parse_rules(blocks[0].splitlines())
        return rules, blocks[1].splitlines()

    def part1(self, args):
        rules, messages = args
        validate = build_validate(rules)
        return sum(validate(message) for message in messages)

    def part2(self, args):
        rules, messages = args
        rules[8] = [[42], [42, 8]]
        rules[11] = [[42, 31], [42, 11, 31]]
        validate = build_validate(rules)
        return sum(validate(message) for message in messages)
