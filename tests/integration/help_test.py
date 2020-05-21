"""Various tests for `candies.cli.command.Command.help`."""

import pytest

from candies.cli.args.arg import Arg
from candies.cli.args.flag import Flag
from candies.cli.cli import cli, CLI
from candies.cli.command import Command

from tests.execution import execute, redirect_stdout


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_default_help_without_description():
    # Arrange.
    @cli
    def main():
        pass

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert out.startswith('usage: main')


def test_default_help_with_description():
    # Arrange.
    @cli
    def main():
        """Here is your help."""

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'Here is your help.' in out


def test_default_help_with_one_argument():
    # Arrange.
    @cli
    def main(x: Arg('description of `x`')):
        return x

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'description of `x`' in out


def test_default_help_with_two_arguments():
    # Arrange.
    @cli
    def main(x: Arg('description of `x`'),
             y: Arg('description of `y`')):
        return x + y

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'description of `x`' in out
    assert 'description of `y`' in out


def test_default_help_with_one_flag():
    # Arrange.
    @cli
    def main(x: Flag('description of `x`')):
        return x

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'description of `x`' in out


def test_default_help_with_two_flags():
    # Arrange.
    @cli
    def main(x: Flag('description of `x`'),
             y: Flag('description of `y`')):
        return x + y

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'description of `x`' in out
    assert 'description of `y`' in out


def test_default_help_with_one_typed_argument():
    # Arrange.
    @cli
    def main(x: Arg[int]('Description of `x`.')):
        return x

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'Description of `x`.' in out


def test_default_help_with_two_typed_arguments():
    # Arrange.
    @cli
    def main(x: Arg[int]('description of `x`'),
             y: Arg[int]('description of `y`')):
        return x + y

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert 'description of `x`' in out
    assert 'description of `y`' in out


def test_default_help_for_subcommand():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def sub():
        pass

    # Act.
    _, out_a = execute(cli, '--help', redirect_stdout)
    _, out_b = execute(cli, 'sub --help', redirect_stdout)

    # Assert.
    assert out_a.startswith('usage: main')
    assert out_b.startswith('usage: main sub')


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
    _, out_a = execute(cli, '--help', redirect_stdout)
    _, out_b = execute(cli, 'sub --help', redirect_stdout)

    # Assert.
    assert out_a == 'main'
    assert out_b.startswith('usage: main sub')


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
    _, out_a = execute(cli, '--help', redirect_stdout)
    _, out_b = execute(cli, 'sub --help', redirect_stdout)

    # Assert.
    assert out_a.startswith('usage: main')
    assert out_b == 'sub'


def test_help_for_argument_with_whitespace_description():
    # Arrange.
    @cli
    def main(x: Arg(' ')):
        pass

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert out.startswith('usage: main')


def test_help_for_argument_with_newline_description():
    # Arrange.
    @cli
    def main(x: Arg('\n\n\n\n')):
        pass

    # Act.
    _, out = execute(cli, '--help', redirect_stdout)

    # Assert.
    assert out.startswith('usage: main')
