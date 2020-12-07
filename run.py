import importlib


def run(args):
    command = args[0]
    input_module = importlib.import_module("input")
    input = getattr(input_module, command)
    solution_module = importlib.import_module(command)
    solution_cls = getattr(solution_module, "Solution")
    solution = solution_cls()
    solution_input = solution.load_data(input)
    if hasattr(solution, "part1"):
        print(solution.part1(solution_input))
    if hasattr(solution, "part2"):
        print(solution.part2(solution_input))


if __name__ == "__main__":
    import sys

    run(sys.argv[1:])
