from argparse import ArgumentParser
from typing import Iterable, Tuple, Any
import inspect

from candies.cli.arg import Arg
from candies.cli.command import Command
from candies.cli.parsers.parser import Parser, Invocation


class StandardParser(Parser):
    """A parser that uses the standard `argparse` package.

    Constructs an instance of `argparse.ArgumentParser` from the provided
    function, and uses it to parse the CLI arguments into key-value pairs.

    For example, for the following function

        def concat(left: Arg('left operand'),
                   right: Arg('right operand')):
            print(left + right)

    an instance of `ArgumentParser` will contain:
        - an argument '-l, --left' with a description 'left operand';
        - an argument '-r, --right' with a description 'right operand'.

    The parser may also be provided with a help text (taken from the function's
    docstring) and default values for arguments.

    Attributes:
        cli: An instance of `CLI` to initialise a parser for.
    """

    def __init__(self, cli):
        self.cli = cli

    def parse(self, args: Iterable[str]) -> Iterable[Invocation]:
        parser = ArgumentParser()

        configure(parser, self.cli.main)

        args = parser.parse_args(list(args))
        args = args.__dict__

        # It's assumed that the entries preserve the insertion order.
        # This feature was introduced in Python 3.7.
        # It's required to be able to differentiate arguments for each command.
        invocations = [Invocation(args={})]

        for key, value in args.items():
            # Read arguments until we find '.command', '..command', etc.
            if key.startswith('.'):
                # `value` may be None in a case
                # if a subcommand was not specified.
                if value is None:
                    break

                invocations[-1].next = value
                invocations.append(Invocation(args={}))
            else:
                invocations[-1].args[key] = value

        return invocations


def configure(parser: ArgumentParser, command: Command, prefix: str = '.'):
    """Configures an `argparse.ArgumentParser` from the specified `command`.

    This function configures an instance of `argparse.ArgumentParser` for
    parsing the provided `command` and adds subparsers for its `subcommands`.
    The names of parsed subcommands are stored as follows:
        1-st level subcommands are stored with a key '.command';
        2-nd level subcommands are stored with a key '..command';
        and so on.

    For example, 'dotnet.py tool install -g something' would be parsed as
        {'.command': 'tool', '..command': 'install', 'g': 'something'}.
    """

    parser.description = command.description

    signature = inspect.signature(command.func)

    # Add parameters to the parser.
    for parameter in signature.parameters.values():
        parser.add_argument(f'-{parameter.name[0]}',
                            f'--{parameter.name}',
                            **dict(configuration(parameter)))

    # Add subparsers to the parser.
    if command.subcommands:
        subparsers = parser.add_subparsers(dest=prefix + 'command')

        for name, subcommand in command.subcommands.items():
            subparser = subparsers.add_parser(name)

            configure(subparser, subcommand, prefix + '.')


def configuration(parameter: inspect.Parameter) -> Iterable[Tuple[str, Any]]:
    """Returns an argument configuration for the specified `parameter`."""

    annotation = parameter.annotation

    if annotation is not None and isinstance(annotation, Arg):
        if annotation.description is not None:
            yield ('help', annotation.description)

    if parameter.default is not parameter.empty:
        yield ('default', parameter.default)
    else:
        yield ('required', True)
