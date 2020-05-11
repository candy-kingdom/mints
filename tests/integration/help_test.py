"""Various tests for `candies.cli.command.Command.help`."""

import sys
from typing import Callable

from candies.cli.args.arg import Arg
from candies.cli.args.flag import Flag
from candies.cli.cli import cli
from candies.cli.command import Command


class Output:
    """Overrides the default `stdout`."""

    def __init__(self):
        self.text = ''

    def write(self, text: str):
        self.text += text


def execute(cli_: Callable, with_: str) -> Output:
    stdout = sys.stdout
    output = sys.stdout = Output()

    try:
        cli_(with_.split())
    except SystemExit as ex:
        if ex.code != 0:
            raise

    sys.stdout = stdout

    return output


def test_default_help_without_description():
    # Arrange.
    @cli
    def main():
        pass

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert output.text.startswith('usage: main')


def test_default_help_with_description():
    # Arrange.
    @cli
    def main():
        """Here is your help."""

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert 'Here is your help.' in output.text


def test_default_help_with_one_argument():
    # Arrange.
    @cli
    def main(x: Arg('description of `x`')):
        return x

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert 'description of `x`' in output.text


def test_default_help_with_two_arguments():
    # Arrange.
    @cli
    def main(x: Arg('description of `x`'),
             y: Arg('description of `y`')):
        return x + y

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert 'description of `x`' in output.text
    assert 'description of `y`' in output.text


def test_default_help_with_one_flag():
    # Arrange.
    @cli
    def main(x: Flag('description of `x`')):
        return x

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert 'description of `x`' in output.text


def test_default_help_with_two_flags():
    # Arrange.
    @cli
    def main(x: Flag('description of `x`'),
             y: Flag('description of `y`')):
        return x + y

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert 'description of `x`' in output.text
    assert 'description of `y`' in output.text


def test_default_help_for_subcommand():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def sub():
        pass

    # Act.
    output_a = execute(main, with_='--help')
    output_b = execute(main, with_='sub --help')

    # Assert.
    assert output_a.text.startswith('usage: main')
    assert output_b.text.startswith('usage: main sub')


def test_custom_help():
    # Arrange.
    @cli
    def main():
        pass

    @main.help
    def help(x: Command):
        return x.name

    @main.command
    def sub():
        pass

    # Act.
    output_a = execute(main, with_='--help')
    output_b = execute(main, with_='sub --help')

    # Assert.
    assert output_a.text == 'main'
    assert output_b.text.startswith('usage: main sub')


def test_custom_help_for_subcommand():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def sub():
        pass

    @sub.help
    def help(command: Command):
        return command.name

    # Act.
    output_a = execute(main, with_='--help')
    output_b = execute(main, with_='sub --help')

    # Assert.
    assert output_a.text.startswith('usage: main')
    assert output_b.text == 'sub'


def test_help_for_argument_with_whitespace_description():
    # Arrange.
    @cli
    def main(x: Arg(' ')):
        pass

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert output.text.startswith('usage: main')


def test_help_for_argument_with_newline_description():
    # Arrange.
    @cli
    def main(x: Arg('\n\n\n\n')):
        pass

    # Act.
    output = execute(main, with_='--help')

    # Assert.
    assert output.text.startswith('usage: main')
