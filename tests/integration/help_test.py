"""Various tests for `candies.cli.command.Command.help`."""

import sys
from typing import Callable, Tuple

from candies.cli.args.arg import Arg
from candies.cli.cli import cli
from candies.cli.command import Command


class Output:
    """Overrides the default `stdout`."""

    def __init__(self):
        self.text = ''

    def write(self, text: str):
        self.text += text


def execute(cli_: Callable, with_: str) -> Tuple[Output, SystemExit]:
    stdout = sys.stdout
    output = sys.stdout = Output()
    error = None

    try:
        cli_(with_.split())
    except SystemExit as ex:
        error = ex

    sys.stdout = stdout

    return output, error


def test_default_help_without_description():
    # Arrange.
    @cli
    def main():
        pass

    # Act.
    output, error = execute(main, with_='--help')

    # Assert.
    assert error.code == 0
    assert output.text.startswith('usage: main')


def test_default_help_with_description():
    # Arrange.
    @cli
    def main():
        """Here is your help."""

    # Act.
    output, error = execute(main, with_='--help')

    # Assert.
    assert error.code == 0
    assert 'Here is your help.' in output.text


def test_default_help_with_one_argument():
    # Arrange.
    @cli
    def main(x: Arg('description of `x`')):
        return x

    # Act.
    output, error = execute(main, with_='--help')

    # Assert.
    assert error.code == 0
    assert 'description of `x`' in output.text


def test_default_help_with_two_arguments():
    # Arrange.
    @cli
    def main(x: Arg('description of `x`'),
             y: Arg('description of `y`')):
        return x + y

    # Act.
    output, error = execute(main, with_='--help')

    # Assert.
    assert error.code == 0
    assert 'description of `x`' in output.text
    assert 'description of `y`' in output.text


def test_custom_help():
    # Arrange.
    @cli
    def main():
        pass

    @main.help
    def help(x: Command):
        return x.name

    # Act.
    output, error = execute(main, with_='--help')

    # Assert.
    assert error.code == 0
    assert output.text == 'main'
