import inspect
import sys
from typing import Callable, Optional, Union, Iterable, Any, Type, Text

from mints.command import Command
from mints.parsers.parser import Parser
from mints.parsers.standard import StandardParser


class CLI:
    """A command line interface.

    Attributes:
        main: A main command to execute.
        parser: A parser to parse command line arguments with
            (`candies.cli.parsers.StandardParser` if not specified).
        parsers: A dictionary that contains parsers for custom types.
            Maps a custom type to a parser itself.
    """

    def __init__(self,
                 main: Optional[Command] = None,
                 parser: Optional[Parser] = None):
        self.main = main
        self.parser = parser
        self.parsers = {}

    def __call__(self,
                 args_or_func: Union[Iterable[str], Callable] = None,
                 **kwargs: Any) -> Any:
        """Either sets a main command or parses the command line arguments
        and executes the main command.

        Args:
            args_or_func: One of the following:
                - An iterable of command line arguments as they would be
                  presented in `sys.argv` (except for the name of the file).
                  For example, an input string 'main.py --a=10 --b=20' should
                  be passed as ['--a=10', '--b=20'].
                  Is set to `argv[1:]` if not specified.
                - A function to be set as the main command of the CLI.
            **kwargs: Options for the main command (such as `name` or
                `description`; refer to the documentation of `Command`
                for a full list of available options).

        Raises:
            `ValueError` when
                - setting the main command when it has already been set;
                - passing `kwargs` along with arguments to run the CLI with;
                - running the CLI when the main command has not been set.

        Examples:
            @cli
            def echo(text: Arg[str]):
                print(text)

            if __name__ == '__main__':
                cli()
        """

        def set(func: Callable) -> Command:
            if self.main is not None:
                raise ValueError(f"Cannot set '{func.__name__}': the main "
                                 f"command has already been set.")

            self.main = Command(func, **kwargs)

            return self.main

        def run(args: Optional[Iterable[str]]) -> Any:
            if kwargs:
                raise ValueError("Cannot run the CLI: "
                                 "`kwargs` are not expected.")
            if self.main is None:
                raise ValueError("Cannot run the CLI: "
                                 "the main command is not set.")

            parser = self.parser or StandardParser(self)
            args = args if args is not None else sys.argv[1:]

            command = self.main
            context = None

            for invoke in parser.parse(args):
                command, context = invoke(command, context)

            return context

        if callable(args_or_func):
            return set(args_or_func)
        else:
            return run(args_or_func)

    def parse(self, func: Callable[[str], Any]) -> Callable[[str], Any]:
        """Defines a parser function for a custom type.

        This method is intended to be used as a function decorator for
        defining parses for custom types (take a look at the `Examples`
        section below).

        Note:
            If you want to add an existing function as a parser or
            add a class with a constructor like `Some.__init__(str)`,
            please refer to the `add_parser` method.

        Args:
            func: A function that converts a string to an instance
                of a custom type. Must have a return type annotation.

        Examples:
            @cli
            def add(money: Arg[Money]):
                ...

            @cli.parse
            def money(x: str) -> Money:
                if x[0] == '$':
                    return Money(float(x[1:]), 'dollars')
                ...
        """
        return self.add_parser(func)

    def add_parser(self, callable: Union[Type, Callable[[str], Any]]) \
            -> Union[Type, Callable[[str], Any]]:
        """Adds a parser for a custom type.

        When a function is provided, this method inspects it and treats
        its return type annotation as the custom type to add a parser for.

        Args:
            callable: Either a parser function or a type.

        Raises:
            `ValueError` if
                - the decorated function has an invalid number of arguments;
                - the decorated function has an invalid argument annotation;
                - the decorated function does not have a return annotation;
                - a parser for the custom type has already been added.

        Examples:
            class Money:
                def __init__(self, value: str):
                    self._value = int(value)

                @staticmethod
                def dollars(value: str):
                    return Money(value[1:])  # Skip '$'.

            @cli
            def main(add: Opt[Money]):
                ...

            # Invokes `Money('$5')` when `--add $5` is specified.
            cli.add_parser(Money)

            # Invokes `Money.dollars('$5')` when `--add $5` is specified.
            cli.add_parser(Money.dollars)
        """

        if isinstance(callable, type):
            type_ = callable
        else:
            signature = inspect.signature(callable)
            parameter = next(iter(signature.parameters.values()), None)

            if len(signature.parameters) != 1:
                raise ValueError(f"Expected a parser function "
                                 f"'{callable.__name__}' "
                                 f"to have a single parameter.")
            if parameter.annotation not in (parameter.default, str, Any, Text):
                raise ValueError(f"Expected a parameter of a parser "
                                 f"function '{callable.__name__}' to be "
                                 f"either empty or 'str', but got "
                                 f"{parameter.annotation}.")

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


cli: CLI = CLI()
"""A default instance of `CLI` for convenient use in most cases."""
