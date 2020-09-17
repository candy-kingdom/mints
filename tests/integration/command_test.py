"""Various tests for `mints.command.Command`."""

from typing import Any

import pytest

from mints.args.arg import Arg
from mints.args.opt import Opt
from mints.args.flag import Flag
from mints.cli import cli, CLI

from tests.execution import execute


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
