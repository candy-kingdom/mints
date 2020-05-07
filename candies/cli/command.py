from typing import Callable, Optional, Union


class Command:
    """A command of a CLI.

    Attributes:
        func: A function to be executed when the command is invoked.
        name: A name of the command
            (`func.__name__` if not explicitly specified).
        description: A description of the command
            (`func.__doc__` if not explicitly specified).
        subcommands: A dictionary that maps a subcommand name
            to the subcommand itself.

    Examples:
        @cli
        def git():
            ...

        @git.command
        def fetch(remote: Arg):
            print(f'Fetching {remote}...')

        @git.command
        def merge(branch: Arg):
            print(f'Merging {branch}...')

        if __name__ == '__main__':
            git('merge --branch develop'.split())
    """

    def __init__(self,
                 func: Callable,
                 name: Optional[str] = None,
                 description: Optional[str] = None):
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__
        self.subcommands = {}

    def command(self,
                func: Optional[Callable] = None,
                name: Optional[str] = None,
                description: Optional[str] = None) -> Union[Callable, 'Command']:
        """Registers a subcommand.

        A subcommand is executed right after the parent one,
        and the latter may also return a value that will be passed
        as an argument to the subcommand.

        Args:
            func: A function to be executed when the subcommand is invoked.
            name: A name of the subcommand
                (`func.__name__` if not explicitly specified).
            description: A description of the subcommand
                (`func.__doc__` if not explicitly specified).
        """

        def define(x):
            command = Command(x, name, description)

            if command.name in self.subcommands:
                raise ValueError(f'A command `{command.name}` has '
                                 f'already been defined.')

            self.subcommands[command.name] = command

            return command

        return define(func) if func is not None else \
               define
