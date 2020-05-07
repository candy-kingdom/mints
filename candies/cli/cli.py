import sys
from typing import Callable, Optional, Union, Iterable

from candies.cli.command import Command
from candies.cli.parsers.parser import Parser
from candies.cli.parsers.standard import StandardParser


class CLI:
    """A command line interface.

    Attributes:
        main: A main command to execute.
        parser: A parser to parse command line arguments with
            (`candies.cli.parsers.StandardParser` if not specified).
    """

    def __init__(self, main: Command, parser: Optional[Parser] = None):
        self.main = main
        self.parser = parser

    def __call__(self, args: Optional[Iterable[str]] = None):
        """Parses the command line arguments and executes the command.

        Args:
            args: A list of command line arguments as they would be presented
                in `sys.argv` (except for the name of the file). For example,
                an input string 'main.py --a=10 --b=20' should be converted to
                ['--a=10', '--b=20'] and passed to this method.
                `argv[1:]` if not explicitly specified.
        """

        parser = self.parser or StandardParser(self)

        command = self.main
        context = None

        for invoke in parser.parse(args or sys.argv[1:]):
            command, context = invoke(command, context)

    def command(self, *args, **kwargs):
        """Defines a subcommand.

        Consider looking at the documentation of the `Command.command` method
        for more details.
        """

        return self.main.command(*args, **kwargs)


def cli(func: Optional[Callable] = None,
        name: Optional[str] = None,
        description: Optional[str] = None) -> Union[Callable, CLI]:
    """Constructs a `CLI` from the specified function.

    Args:
        func: A function to construct a `CLI` from.
        name: A name of the main command.
        description: A description of the main command.

    Returns:
        Either an instance of `CLI` if `func` was specified
        or a decorator to wrap a function with.

    Examples:
        @cli
        def git(version):
            ...
    """

    def wrap(x):
        return CLI(Command(x, name, description))

    return wrap(func) if func is not None else \
           wrap
