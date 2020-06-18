from abc import ABCMeta, abstractmethod
from typing import Iterable, Dict, Any, Optional, Tuple

from mints.command import Command


class Invocation:
    """An invocation of a CLI command.

    Attributes:
        args: A dictionary of arguments that maps arguments' names to values.
        next: A name of the command to be executed next.
    """

    def __init__(self, args: Dict[str, Any], next: Optional[str] = None):
        self.args = args
        self.next = next

    def __repr__(self):
        return f'Invocation(' \
               f'args={repr(self.args)}, ' \
               f'next={repr(self.next)}' \
               f')'

    def __call__(self, command: Command, context: Any) \
            -> Tuple[Optional[Command], Any]:
        """Invokes the `command` with the provided `context`.

        Args:
            command: An instance of a `Command` to execute.
            context: A context to execute the `command` with.

        Returns:
            A pair of (<next-command>, <next-context>).
        """

        if context is not None:
            raise NotImplementedError

        context = command.func(**self.args)

        if self.next is not None:
            return command.subcommands[self.next], context
        else:
            return None, context


class Parser(metaclass=ABCMeta):
    """A parser for command line arguments."""

    @abstractmethod
    def parse(self, args: Iterable[str]) -> Iterable[Invocation]:
        """Parses the specified arguments.

        Args:
            args: A list of command line arguments as they would be presented
                in `sys.argv` (except for the name of the file). For example,
                an input string 'main.py --a=10 --b=20' should be converted to
                ['--a=10', '--b=20'] and passed to this method.

        Returns:
            A collection of `Invocation`s. For example, an input string
            'git.py --no-pager fetch --remote origin' could be parsed as

                [
                    Invocation(args={'no-pager': True}, next='fetch'),
                    Invocation(args={'remote': 'origin'})
                ]
        """
