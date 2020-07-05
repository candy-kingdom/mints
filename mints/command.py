import inspect
from typing import Callable, Optional, Union, Any


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
            cli('merge --branch develop'.split())
    """

    def __init__(self,
                 func: Callable,
                 name: Optional[str] = None,
                 description: Optional[str] = None):
        self.func = func
        self.name = name or func.__name__
        self.help_ = None
        self.description = description or func.__doc__
        self.subcommands = {}
        self.catches = {}

    def command(self,
                func: Optional[Callable] = None,
                name: Optional[str] = None,
                description: Optional[str] = None) \
            -> Union[Callable, 'Command']:
        """Defines a subcommand.

        A subcommand is executed right after the parent one,
        and the latter may also return a value that will be passed
        as an argument to the subcommand.

        Args:
            func: A function to be executed when the subcommand is invoked.
            name: A name of the subcommand
                (`func.__name__` if not explicitly specified).
            description: A description of the subcommand
                (`func.__doc__` if not explicitly specified).

        Returns:
            Either an instance of `Command` if `func` was specified
            or a decorator to wrap a function with.
        """

        def define(x):
            command = Command(x, name, description)

            if command.name in self.subcommands:
                raise ValueError(f'A command `{command.name}` has '
                                 f'already been defined.')

            self.subcommands[command.name] = command

            return command

        return define(func) if func is not None else define

    def help(self, func: Callable[['Command'], str]) -> Callable:
        """Defines a callable to be called for `--help`.

        The callable must be able to accept a command to construct a help
        message for and return a string with the message to be displayed.

        Args:
            func: A callable to be called when `--help` is specified.

        Returns:
            The `func` that was specified.

        Examples:
            @cli
            def magic(spell):
                ...

            @magic.help
            def help(command):
                return f'Help for "{command.name}" is yet to be done. ' \
                       f'Please stand by.'
        """

        self.help_ = func

        return func

    def catch(self, func: Callable[[BaseException], Any]) -> Callable:
        """Defines a function to handle errors of specific types
        raised during execution of the command.

        This method is designed to be used as a decorator.

        The decorated function must have a single parameter. This parameter
        must be annotated with the type of an exception that the function
        will handle (the annotation may also be a union of exception types).

        The decorated function will be called to handle errors raised during
        execution of the command or its subcommands (unless a subcommand
        catches that error by itself).

        Args:
            func: A function to handle errors with.

        Returns:
            The decorated function.

        Raises:
            `ValueError` if
                - the decorated function has an invalid amount of parameters;
                - the decorated function parameter is not annotated;
                - an error handler for an exception has already been defined.

        Example:
            @cli
            def divide(x: Arg[int], y: Arg[int]):
                print(x / y)

            @divide.catch
            def _(error: ZeroDivisionError):
                print('Division by zero is not defined.')
        """

        signature = inspect.signature(func)
        parameter = next(iter(signature.parameters.values()), None)

        if len(signature.parameters) != 1:
            raise ValueError(f'Expected a function with a single parameter, '
                             f'but got with {len(signature.parameters)}.')
        if parameter.annotation is parameter.empty:
            raise ValueError(f'Expected the first argument of '
                             f'a function to be annotated.')

        def catch(exception):
            if exception in self.catches:
                raise ValueError(f'An error handler for {exception} '
                                 f'has already been defined.')

            self.catches[exception] = func

        annotation = parameter.annotation

        if getattr(annotation, '__origin__', None) is Union:
            for exception in annotation.__args__:
                catch(exception)
        else:
            catch(annotation)

        return func
