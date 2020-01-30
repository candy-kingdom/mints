import inspect


def cli(x):
    print(inspect.signature(x))
