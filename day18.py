import re
from dataclasses import dataclass

from base import BaseSolution


TOKEN_RE = re.compile(r"[0-9\+\*\(\)]")


class Expression:
    def evaluate(self):
        pass


class Value(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class Operator(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


class Add(Operator):
    def evaluate(self):
        lhs_value = self.lhs.evaluate()
        rhs_value = self.rhs.evaluate()
        return lhs_value + rhs_value


class Mul(Operator):
    def evaluate(self):
        lhs_value = self.lhs.evaluate()
        rhs_value = self.rhs.evaluate()
        return lhs_value * rhs_value


def build_tree(tokens):
    stack = [[]]
    for tok in tokens:
        if tok == "(":
            stack.append([])
        elif tok == ")":
            sub = stack.pop()
            sub = list(reversed(sub))
            stack[-1].append(sub)
        else:
            stack[-1].append(tok)
    return list(reversed(stack[0]))


def build_expression(tree):
    if isinstance(tree[0], list):
        lhs = build_expression(tree[0])
    else:
        lhs = Value(int(tree[0]))
    if not tree[2:]:
        return lhs
    rhs = build_expression(tree[2:])
    if tree[1] == "+":
        return Add(lhs, rhs)
    if tree[1] == "*":
        return Mul(lhs, rhs)


def evaluate(line):
    tokens = TOKEN_RE.findall(line)
    tree = build_tree(tokens)
    expression = build_expression(tree)
    return expression.evaluate()


class Solution(BaseSolution):
    def load_data(self, input):
        return input.splitlines()

    def part1(self, data):
        return sum(evaluate(line) for i, line in enumerate(data))
