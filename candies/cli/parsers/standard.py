from argparse import ArgumentParser, HelpFormatter
from typing import Iterable, Any, Callable, Type, Dict, Union, Optional, Tuple
import inspect

from candies.cli.args.arg import Arg
from candies.cli.args.flag import Flag
from candies.cli.args.opt import Opt
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
        parser = configured(new_parser, self.cli.main)

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


def help(command: Command) -> Type[HelpFormatter]:
    """Constructs a subclass of `argparse.HelpFormatter` for `command`."""

    class Help(HelpFormatter):
        """Defines a format of the `--help` message."""

        def format_help(self):
            if command.help_ is not None:
                return command.help_(command)
            else:
                return super(Help, self).format_help()

    return Help


def new_parser(*args, **kwargs) -> ArgumentParser:
    """Creates a new parser."""
    return ArgumentParser(*args, **kwargs)


def new_subparser(subparsers: Any) -> Callable[[Any], ArgumentParser]:
    """Returns a function to create a new subparser."""
    return subparsers.add_parser


def configured(new: Callable, command: Command, prefix: str = '.') \
        -> ArgumentParser:
    """Configures an `argparse.ArgumentParser` from the specified `command`.

    This function configures an instance of `argparse.ArgumentParser` for
    parsing the provided `command`, and adds subparsers for its `subcommands`.
    The names of parsed subcommands are stored as follows:
        1-st level subcommands are stored with a key '.command';
        2-nd level subcommands are stored with a key '..command';
        and so on.

    For example, 'dotnet.py tool install -g something' would be parsed as
        {'.command': 'tool', '..command': 'install', 'g': 'something'}.
    """

    parser = new(command.name,
                 description=command.description,
                 formatter_class=help(command))

    def short_of(x: Any) -> Optional[str]:
        short = getattr(x, 'short', None)

        if short is None:
            # If `None`, then considered as omitted.
            return short

        if short == '':
            raise ValueError(f"Flag '{parameter.name}' has invalid short name "
                             f"'{short}': "
                             f"it is an empty string")

        if len(short) > 1:
            raise ValueError(f"Flag '{parameter.name}' has invalid short name "
                             f"'{short}': "
                             f"it consists of more than one character")

        if not short.isalpha():
            raise ValueError(f"Flag '{parameter.name}' has invalid short name "
                             f"'{short}': "
                             f"it is not an alphabet character")

        return short

    def prefixes_of(x: Any) -> Tuple[str, str]:
        # TODO: Add more prefixes depending on `prefix` attribute.
        return '-', '--'

    def is_(x: Any, of: Type) -> bool:
        return isinstance(x, of) or x == of

    def configure_arg(x: inspect.Parameter, config: Dict):
        parser.add_argument(x.name, **config)

    def configure_named_arg(x: inspect.Parameter, config: Dict):
        short = short_of(x.annotation)
        short_prefix, long_prefix = prefixes_of(x.annotation)

        if short is None:
            parser.add_argument(f'{long_prefix}{x.name}',
                                **config)
        else:
            parser.add_argument(f'{long_prefix}{x.name}',
                                f'{short_prefix}{short}',
                                **config)

    def configure_flag(x: inspect.Parameter, config: Dict):
        # This actually makes an arg to behave like a flag,
        # so one could call `--x` instead of `--x y`.
        config['action'] = 'store_true'

        if x.default is x.empty:
            config['default'] = False
        else:
            config['default'] = bool(x.default)

        configure_named_arg(x, config)

    def configure_opt(x: inspect.Parameter, config: Dict):
        if x.default is not x.empty:
            config['default'] = x.default
            config['required'] = False
        else:
            config['required'] = True

        configure_named_arg(x, config)

    signature = inspect.signature(command.func)

    # Add parameters to the parser.
    for parameter in signature.parameters.values():
        config = {}

        description = getattr(parameter.annotation, 'description', None)
        if description is not None:
            config['help'] = description

        if is_(parameter.annotation, Arg):
            configure_arg(parameter, config)

        if is_(parameter.annotation, Flag):
            configure_flag(parameter, config)

        if is_(parameter.annotation, Opt):
            configure_opt(parameter, config)

    # Add subparsers to the parser.
    if command.subcommands:
        subparsers = parser.add_subparsers(dest=prefix + 'command')

        for name, subcommand in command.subcommands.items():
            _ = configured(new_subparser(subparsers), subcommand, prefix + '.')

    return parser
