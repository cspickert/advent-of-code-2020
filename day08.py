from base import BaseSolution


class BadInstruction(Exception):
    pass


class Solution(BaseSolution):
    def load_data(self, input):
        program = []
        for line in input.splitlines():
            op, arg = line.split()
            program.append((op, int(arg)))
        return program

    def run(self, program):
        pos, acc = 0, 0
        visited = set()
        while pos < len(program) and pos not in visited:
            visited.add(pos)
            op, arg = program[pos]
            if op == "acc":
                acc += arg
                pos += 1
            elif op == "jmp":
                if arg == 0:
                    raise BadInstruction(op, arg)
                pos += arg
            elif op == "nop":
                pos += 1
        return pos, acc

    def part1(self, program):
        _, acc = self.run(program)
        return acc

    def part2(self, program):
        patches = []
        for pos, (ins, arg) in enumerate(program):
            if ins == "jmp":
                patches.append((pos, ("nop", arg)))
            elif ins == "nop":
                patches.append((pos, ("jmp", arg)))
        for patch in patches:
            patched_program = program[:]
            patched_program[patch[0]] = patch[1]
            try:
                pos, acc = self.run(patched_program)
            except BadInstruction:
                pass
            if pos == len(patched_program):
                return acc
        return None
