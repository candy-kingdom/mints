"""Various tests for `candies.cli.args.arg.Arg`."""

from typing import Callable, Any

from candies.cli.cli import cli
from candies.cli.args.arg import Arg


def execute(cli_: Callable, with_: str) -> Any:
    try:
        return cli_(with_.split())
    # `BaseException`, because `argparse` calls `exit` on error.
    except BaseException as e:
        return e


def test_no_arguments():
    # Arrange.
    @cli
    def main():
        return True

    # Act.
    cx = execute(main, with_='')

    # Assert.
    assert cx


def test_argument_without_annotation():
    # Arrange.
    @cli
    def main(x):
        return x

    # Act.
    cx = execute(main, with_='whatever')

    # Assert.
    assert isinstance(cx, ValueError)


def test_one_arg():
    # Arrange.
    @cli
    def main(x: Arg):
        return x

    # Act.
    cx = execute(main, with_='1')

    # Assert.
    assert cx == '1'


def test_one_arg_with_description():
    # Arrange.
    @cli
    def main(x: Arg('Description.')):
        return x

    # Act.
    cx = execute(main, with_='1')

    # Assert.
    assert cx == '1'


def test_two_args():
    # Arrange.
    @cli
    def main(x: Arg, y: Arg):
        return x, y

    # Act.
    cx = execute(main, with_='1 2')

    # Assert.
    assert cx == ('1', '2')


def test_one_arg_with_default_value():
    # Arrange.
    @cli
    def main(x: Arg = '1'):
        return x

    # Act.
    ex = execute(main, with_='')

    # Assert.
    assert isinstance(ex, BaseException)


def test_two_args_but_called_with_one():
    # Arrange.
    @cli
    def main(x: Arg):
        return x

    # Act.
    ex = execute(main, with_='1 2')

    # Assert.
    assert isinstance(ex, BaseException)


def test_one_arg_but_called_with_two():
    # Arrange.
    @cli
    def main(x: Arg):
        return x

    # Act.
    ex = execute(main, with_='1 2')

    # Assert.
    assert isinstance(ex, BaseException)
