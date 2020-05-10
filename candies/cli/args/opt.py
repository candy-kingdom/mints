from typing import Type

from candies.cli.args.typed import Typed


class Opt:
    """A command line argument that represents an option.

    Options are used in same way as named arguments.
    They can be considered as flags (see `Flag`) with explicit values.

    For example, in the following line:

        $ say "Hello, world!" --times 3

    `--times` is an option with value of `3`.

    Attributes:
        description (str): A description of an option. Shown in the help page.
        short (str): A short form of an option.
            Must be non empty and consist of 1 alphabet character.

    Examples:
        # To handle the mentioned above CLI, one could write:
        @cli
        def say(phrase: Arg, times: Opt):
            ...
    """

    def __init__(self, description: str = None, short: str = None):
        self.description = description
        self.short = short

    def __class_getitem__(cls, type: Type) -> Typed:
        return Typed(cls, type)
