from argparse import ArgumentParser
from typing import List, Any, Iterable, Callable, Dict
import inspect

from candies.cli.arg import Arg
from candies.cli.parsers.parser import Parser


class StandardParser(Parser):
    """A parser that uses the standard `argparse` package.

    Constructs an instance of `argparse.ArgumentParser` from the provided
    function, and uses it to parse the CLI arguments into key-value pairs.

    For example, for the following function

        def concat(left: Arg['left operand'], right: Arg['right operand']):
            print(left + right)

    an instance of `ArgumentParser` will contain:
        - an argument '-l, --left' with a description 'left operand';
        - an argument '-r, --right' with a description 'right operand'.

    The parser may also be provided with a help text (taken from the function's
    docstring) and default values for arguments.

    Args:
        func (function): A function to construct an instance of
            `ArgumentParser` from.
    """

    def __init__(self, func: Callable):
        self._func = func

    def parse(self, args: List[str]) -> Dict[str, Any]:
        signature = inspect.signature(self._func)

        parser = ArgumentParser()
        parser.description = self._func.__doc__

        # Add parameters to the parser.
        for parameter in signature.parameters.values():
            parser.add_argument(f'-{parameter.name[0]}',
                                f'--{parameter.name}',
                                **dict(configuration(parameter)))

        args = parser.parse_args(args)
        args = args.__dict__

        return args


def configuration(parameter: inspect.Parameter) -> Iterable[Any]:
    """Returns an argument configuration for the specified `parameter`."""

    annotation = parameter.annotation

    if annotation is not None and isinstance(annotation, Arg):
        if annotation.description is not None:
            yield ('help', annotation.description)

    if parameter.default is not parameter.empty:
        yield ('default', parameter.default)
    else:
        yield ('required', True)
