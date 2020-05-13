"""Various tests for `candies.cli.args.arg.Arg`."""

from typing import Any

import pytest

from candies.cli.cli import cli, CLI
from candies.cli.args.arg import Arg

from tests.execution import execute, redirect_stderr


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_no_args():
    # Arrange.
    @cli
    def main():
        return True

    # Act.
    cx = execute(cli, with_='')

    # Assert.
    assert cx


def test_arg_without_annotation():
    # Arrange.
    @cli
    def main(x):
        return x

    # Act.
    ex = execute(cli, with_='')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' must have an annotation" in str(ex)


def test_one_arg():
    # Arrange.
    @cli
    def main(x: Arg):
        return x

    # Act.
    cx = execute(cli, with_='1')

    # Assert.
    assert cx == '1'


def test_one_arg_with_description():
    # Arrange.
    @cli
    def main(x: Arg('Description.')):
        return x

    # Act.
    cx = execute(cli, with_='1')

    # Assert.
    assert cx == '1'


def test_two_args():
    # Arrange.
    @cli
    def main(x: Arg, y: Arg):
        return x, y

    # Act.
    cx = execute(cli, with_='1 2')

    # Assert.
    assert cx == ('1', '2')


def test_one_arg_with_default_value():
    # Arrange.
    @cli
    def main(x: Arg = '1'):
        return x

    # Act.
    ex, err = execute(cli, '', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert "required: x" in err


def test_two_args_but_called_with_one():
    # Arrange.
    @cli
    def main(x: Arg, y: Arg):
        return x, y

    # Act.
    ex, err = execute(cli, '1', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'required: y' in err


def test_one_arg_but_called_with_two():
    # Arrange.
    @cli
    def main(x: Arg):
        return x

    # Act.
    ex, err = execute(cli, '1 2', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'unrecognized arguments: 2' in err
