import inspect
import sys
from typing import Callable, Optional, Union, Iterable, Any, Type

from candies.cli.command import Command
from candies.cli.parsers.parser import Parser
from candies.cli.parsers.standard import StandardParser


class CLI:
    """A command line interface.

    Attributes:
        main: A main command to execute.
        parser: A parser to parse command line arguments with
            (`candies.cli.parsers.StandardParser` if not specified).
        parsers: A dictionary that contains parsers for custom types.
            Maps a custom to a parser itself.
    """

    def __init__(self, main: Command, parser: Optional[Parser] = None):
        self.main = main
        self.parser = parser
        self.parsers = {}

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
        args = args if args is not None else sys.argv[1:]

        command = self.main
        context = None

        for invoke in parser.parse(args):
            command, context = invoke(command, context)

        return context

    def command(self, *args, **kwargs):
        """Defines a subcommand.

        Consider looking at the documentation of the `Command.command` method
        for more details.
        """
        return self.main.command(*args, **kwargs)

    def help(self, *args, **kwargs):
        """Defines a function to be called for `--help`.

        Consider looking at the documentation of the `Command.help` method
        for more details.
        """
        return self.main.help(*args, **kwargs)

    def parse(self, callable: Union[Callable[[str], Any], Type]) \
            -> Union[Type, Callable[[str], Any]]:
        """Defines a parser for a custom type.

        Args:
            callable: A callable that converts a string to an instance
                of a custom type. For example, a parser function or a
                type that accepts a string to a constructor.

        Examples:
            @cli
            def add(money: Arg[Money]):
                ...

            @main.parse
            def money(x: str) -> Money:
                if x[0] == '$':
                    return Money(float(x[1:]), 'dollars')
                ...

            # Or, as an alternative, if
            # `Money.__init__(str)` can be called.
            main.parse(Money)
        """

        if isinstance(callable, type):
            type_ = callable
        else:
            signature = inspect.signature(callable)

            if len(signature.parameters) != 1:
                raise ValueError(f"Expected a parser function "
                                 f"'{callable.__name__}' "
                                 f"to have a single parameter.")

            type_ = signature.return_annotation

            if type_ is signature.empty:
                raise ValueError(f"Expected a parser function "
                                 f"'{callable.__name__}' "
                                 f"to have a return annotation.")

        if type_ in self.parsers:
            name = getattr(self.parsers[type_], '__name__', None)
            name = name or str(type(self.parsers[type_]))

            raise ValueError(f"A parser for the type '{type_}' "
                             f"has already been added "
                             f"(namely '{name}').")

        self.parsers[type_] = callable

        return callable


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
