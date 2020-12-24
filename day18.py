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


def build_tree(tokens, add_precedence=False):
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


def build_add_precedence(tree):
    tree = [
        build_add_precedence(node) if isinstance(node, list) else node for node in tree
    ]
    start = 0
    while start < len(tree):
        try:
            index = tree.index("+")
            tree[index - 1 : index + 2] = [tree[index - 1 : index + 2]]
            start = index + 1
        except ValueError:
            break
    return tree


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


def evaluate(line, add_precedence=False):
    tokens = TOKEN_RE.findall(line)
    tree = build_tree(tokens)
    if add_precedence:
        tree = build_add_precedence(tree)
    expression = build_expression(tree)
    return expression.evaluate()


class Solution(BaseSolution):
    def load_data(self, input):
        return input.splitlines()

    def part1(self, data):
        return sum(evaluate(line) for line in data)

    def part2(self, data):
        return sum(evaluate(line, add_precedence=True) for line in data)
