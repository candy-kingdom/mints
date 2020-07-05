"""Various tests for `candies.cli.command.Command`."""

import pytest

from mints.args.arg import Arg
from mints.args.opt import Opt
from mints.args.flag import Flag
from mints.cli import cli, CLI

from tests.execution import execute, redirect_stdout


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_nonexistent_command_name():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def one():
        pass

    @main.command
    def two():
        pass

    # Act.
    cx = execute(cli, 'three')

    # Assert.
    assert isinstance(cx, SystemExit)


def test_nonexistent_subcommand_name():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def one():
        pass

    @main.command
    def two():
        pass

    @one.command
    def a():
        pass

    @two.command
    def b():
        pass

    # Act.
    cx = execute(cli, 'one b')

    # Assert.
    assert isinstance(cx, SystemExit)


def test_multiple_subcommands():
    # Arrange.
    @cli
    def main(x: Flag):
        pass

    @main.command
    def first(y: Arg[int]):
        pass

    @first.command
    def second(z: Opt[int]):
        return z

    # Act.
    cx = execute(cli, '--x first 1 second --z 2')

    # Assert.
    assert cx == 2


def test_one_command_without_arguments():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def sub():
        return True

    # Act.
    cx = execute(cli, 'sub')

    # Assert.
    assert cx is True


def test_one_command_with_arguments():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def sub(x: Arg[int], y: Opt[int], z: Flag):
        return x, y, z

    # Act.
    cx = execute(cli, 'sub 1 --y 2 --z')

    # Assert.
    assert cx == (1, 2, True)


def test_two_commands_without_arguments():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def one():
        return True

    @main.command
    def two():
        return False

    # Act.
    cx_a = execute(cli, 'one')
    cx_b = execute(cli, 'two')

    # Assert.
    assert cx_a is True
    assert cx_b is False


def test_two_commands_with_same_arguments():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def one(x: Arg[int], y: Opt[int], z: Flag):
        return +x, +y, z

    @main.command
    def two(x: Arg[int], y: Opt[int], z: Flag):
        return -x, -y, z

    # Act.
    cx_a = execute(cli, 'one 1 --y 2 --z')
    cx_b = execute(cli, 'two 1 --y 2 --z')

    # Assert.
    assert cx_a == (+1, +2, True)
    assert cx_b == (-1, -2, True)


def test_two_commands_with_different_arguments():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def one(x: Arg[int], y: Opt[int], z: Flag):
        return +x, +y, z

    @main.command
    def two(a: Arg[int], b: Opt[int], c: Flag):
        return -a, -b, c

    # Act.
    cx_a = execute(cli, 'one 1 --y 2 --z')
    cx_b = execute(cli, 'two 1 --b 2 --c')

    # Assert.
    assert cx_a == (+1, +2, True)
    assert cx_b == (-1, -2, True)


def test_command_raising_exception():
    # Arrange.
    @cli
    def main():
        raise ValueError('Message.')

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert isinstance(cx, ValueError)
    assert cx.args == ('Message.',)


def test_subcommand_raising_exception():
    # Arrange.
    @cli
    def one():
        pass

    @one.command
    def two():
        raise ValueError('Message.')

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert isinstance(cx, ValueError)
    assert cx.args == ('Message.',)


def test_command_and_subcommand_raising_exception():
    # Arrange.
    @cli
    def one():
        raise ValueError('One.')

    @one.command
    def two():
        raise ValueError('Two.')

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert isinstance(cx, ValueError)
    assert cx.args == ('One.',)


def test_command_catching_exception_of_exact_type():
    # Arrange.
    @cli
    def main():
        raise ValueError('Message.')

    @main.catch
    def _(error: Exception):
        return 'Whatever.'

    @main.catch
    def _(error: ValueError):
        return error.args

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == ('Message.',)


def test_command_catching_exception_of_base_type():
    # Arrange.
    @cli
    def main():
        raise ValueError('Message.')

    @main.catch
    def _(error: Exception):
        return error.args

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == ('Message.',)


def test_command_not_catching_exception_of_different_type():
    # Arrange.
    @cli
    def main():
        raise ValueError('Message.')

    @main.catch
    def _(error: TypeError):
        return 'Whatever.'

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert isinstance(cx, ValueError)
    assert cx.args == ('Message.',)


def test_command_not_catching_exception_raised_when_handling_other_exception():
    # Arrange.
    @cli
    def main():
        raise ValueError('Message.')

    @main.catch
    def _(error: ValueError):
        raise TypeError()

    @main.catch
    def _(error: TypeError):
        return 'Whatever.'

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert isinstance(cx, TypeError)


def test_command_catching_exception_of_subcommand():
    # Arrange.
    @cli
    def one():
        pass

    @one.command
    def two():
        raise ValueError('Message.')

    @one.catch
    def _(error: Exception):
        return 'Whatever.'

    @one.catch
    def _(error: ValueError):
        return error.args

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert cx == ('Message.',)


def test_command_halting_execution_after_catching_exception():
    # Arrange.
    @cli
    def one():
        raise ValueError('Message.')

    @one.command
    def two():
        print('Whatever.')

    @one.catch
    def _(error: ValueError):
        return error.args

    # Act.
    cx, out = execute(cli, 'two', redirect_stdout)

    # Assert.
    assert cx == ('Message.',)
    assert out == ''


def test_subcommand_catching_exception_of_exact_type():
    # Arrange.
    @cli
    def one():
        pass

    @one.command
    def two():
        raise ValueError('Message.')

    @two.catch
    def _(error: Exception):
        return 'Whatever.'

    @two.catch
    def _(error: ValueError):
        return error.args

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert cx == ('Message.',)


def test_subcommand_catching_exception_of_base_type():
    # Arrange.
    @cli
    def one():
        pass

    @one.command
    def two():
        raise ValueError('Message.')

    @two.catch
    def _(error: Exception):
        return error.args

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert cx == ('Message.',)


def test_subcommand_not_catching_exception_of_different_type():
    # Arrange.
    @cli
    def one():
        pass

    @one.command
    def two():
        raise ValueError('Message.')

    @one.catch
    def _(error: TypeError):
        return 'One.'

    @two.catch
    def _(error: TypeError):
        return 'Two.'

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert isinstance(cx, ValueError)
    assert cx.args == ('Message.',)


def test_command_catching_exception_raised_when_subcommand_handling_other_exception():
    # Arrange.
    @cli
    def one():
        pass

    @one.command
    def two():
        raise ValueError('Two.')

    @one.catch
    def _(error: ValueError):
        return error.args

    @two.catch
    def _(error: ValueError):
        raise ValueError('One.')

    # Act.
    cx = execute(cli, 'two')

    # Assert.
    assert cx == ('One.',)
