from typing import Type

from mints.args.typed import Typed


class Opt:
    """A command line argument that represents an option.

    Options are used in same way as named arguments.
    They can be considered as flags (see `Flag`) with explicit values.

    For example, in the following line:

        $ say "Hello, world!" --times 3

    `--times` is an option with value of `3`.

    Attributes:
        description: A description of an option. Shown in the help page.
        short: A short form of an option.
            Must be non empty and consist of 1 alphabet character.
        prefix: A string that represents a prefix of an option.
            It should contain only 1 character.
            For example, a value of `+` allows `++value 2` and `+v 2`
            notation.
            Default is '-'.

    Examples:
        # To handle the mentioned above CLI, one could write:
        @cli
        def say(phrase: Arg, times: Opt):
            ...
    """

    def __init__(self, description: str = None, short: str = None, prefix: str = '-'):
        self.description = description
        self.short = short
        self.prefix = prefix

    def __class_getitem__(cls, type: Type) -> Typed:
        return Typed(cls, type)
