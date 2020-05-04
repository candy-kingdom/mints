import sys
from typing import List, Callable, Optional, Union

from candies.cli.parsers import Parser, StandardParser


class CLI:
    """A command line interface.

    Examples:
        @cli
        def main(a: Arg['description'],
                 b: Arg['description'] = 'default'):
            \"""Some help text.\"""
            ...

        if __name__ == '__main__':
            main()
    """

    def __init__(self, main):
        self._main = main

    def __call__(self, args: List[str] = None, parser: Parser = None):
        """Parses the specified arguments and calls the wrapped function."""

        if parser is None:
            parser = StandardParser(self._main)

        args = parser.parse(args or sys.argv[1:])

        # Note: this approach does not handle `--help`.
        return self._main(**args)

    def command(self, func):
        raise NotImplementedError


def cli(func: Optional[Callable] = None) -> Union[Callable, CLI]:
    """Constructs a CLI from the specified function.

    Args:
        func (function, optional): A function to construct a CLI from.

    Returns:
        Either an instance of `CLI` if `func` was specified or a decorator
        to wrap a function with.

    Examples:
        @cli
        def fetch(branch):
            ...
    """

    if func is None:
        return \
            lambda x: CLI(x)
    else:
        return CLI(func)
