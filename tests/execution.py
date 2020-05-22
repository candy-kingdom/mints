from typing import Any, Callable, ContextManager, Optional, List
import contextlib
import io


def execute(cli: Callable[[List[str]], Any],
            with_: str,
            redirect: Optional[Callable[[Any], ContextManager]] = None) \
        -> Any:
    """Executes the CLI callable with the specified command line.

    Supports redirection of either `sys.stdout` or `sys.stderr` for testing
    purposes.

    Args:
        cli: A callable that represents a CLI function.
        with_: A string that represents a command line.
        redirect: An object that redirects an output into file-like object
            using context manager protocol.

    Returns:
        One of the following:
            - a result of the CLI execution;
            - an exception object if the execution has thrown an error.
        If the `redirect` object is specified, the functions returns a tuple
        with the actual result and redirect output as text.

    Examples:
        result = execute(cli, '--x')
        result, err = execute(cli, '--x', redirect_stderr)
        result, out = execute(cli, '--x', redirect_stdout)

    Todo:
        * If needed, extend the `redirect` argument to an iterable for
            redirecting both `sys.stdout` and `sys.stderr`.
    """

    def execute_with(redirect: Callable[[Any], ContextManager]):
        output = io.StringIO()

        with redirect(output):
            result = execute_()

        return result, output.getvalue()

    def execute_():
        try:
            return cli(with_.split())
        # `BaseException`, because `argparse` throws `SystemExit` on error.
        except BaseException as e:
            return e

    return execute_with(redirect) if redirect is not None else \
           execute_()


# Dummy objects that are used only for the following syntax:
#     execute(cli, 'args', redirect_stdout)
#     execute(cli, 'args', redirect_stderr)
redirect_stdout = contextlib.redirect_stdout
redirect_stderr = contextlib.redirect_stderr
