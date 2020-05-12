from typing import Any, Callable
import contextlib
import io
import sys


def execute(cli: Callable[[str], Any],
            with_: str,
            redirect: Any = None) -> Any:

    def execute_with(redirect: Any):
        output = io.StringIO()

        with redirect(output):
            result = execute_()

        return result, output.getvalue()

    def execute_():
        try:
            return cli(with_.split())
        # `BaseException`, because `argparse` calls `exit` on error.
        except BaseException as e:
            return e

    return execute_with(redirect) if redirect is not None else \
           execute_()


# Dummy objects that are used only for the following syntax:
#     execute(cli, with_='args', redirect_stdout)
redirect_stdout = contextlib.redirect_stdout
redirect_stderr = contextlib.redirect_stderr
