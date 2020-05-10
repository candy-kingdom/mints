from typing import Callable, Any

from candies.cli.args.arg import Arg
from candies.cli.args.opt import Opt
from candies.cli.cli import cli


def execute(cli_: Callable, with_: str) -> Any:
    cli_(with_.split())

    try:
        return cli_(with_.split())
    # `BaseException`, because `argparse` calls `exit` on error.
    except BaseException as e:
        return e


def test_typed_arg_without_description():
    # Arrange.
    @cli
    def main(x: Arg[int]):
        return x

    # Act.
    cx = execute(main, with_='10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_arg_with_description():
    # Arrange.
    @cli
    def main(x: Arg[int]('Description.')):
        return x

    # Act.
    cx = execute(main, with_='10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_opt_without_description():
    # Arrange.
    @cli
    def main(x: Opt[int]):
        return x

    # Act.
    cx = execute(main, with_='--x 10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_opt_with_description():
    # Arrange.
    @cli
    def main(x: Opt[int]('Description.')):
        return x

    # Act.
    cx = execute(main, with_='--x 10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10
