from typing import Type

from mints.args.typed import Typed


class Arg:
    """A positional argument of a command line.

    In CLI, positional arguments are specified without explicit names,
    similarly as they do in regular functions.

    For example, in the following call:

        $ mv 1.txt 2.txt

    '1.txt' and '2.txt' are positional arguments.

    Note:
        This class intended to be used as a type annotation in CLI functions
        to help the parser distinguish simple arguments, flags, prompts, etc.

        Consider looking at the documentation of the `candies.cli.CLI` class
        for more details about which kinds of CLIs the `Arg` produces.

    Attributes:
        description: A description of an argument. Shown in help page.

    Examples:
        @cli
        def main(a: Arg('argument a'),
                 b: Arg('argument b')):
            ...
    """

    def __init__(self, description: str = None):
        self.description = description

    def __class_getitem__(cls, type: Type) -> Typed:
        return Typed(cls, type)
