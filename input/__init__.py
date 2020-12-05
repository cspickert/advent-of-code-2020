import os.path

input_dir = os.path.dirname(os.path.realpath(__file__))


def file_contents(filename):
    with open(os.path.join(input_dir, filename)) as f:
        return f.read()


def __getattr__(name):
    return file_contents(f"{name}.txt")
