"""Various tests for `candies.cli.command.Command`."""

from typing import Any

import pytest

from candies.cli.args.arg import Arg
from candies.cli.args.opt import Opt
from candies.cli.args.flag import Flag
from candies.cli.cli import cli, CLI


def execute(with_: str) -> Any:
    try:
        return cli(with_.split())
    # `SystemExit`, because `argparse` calls `exit` on error.
    except SystemExit as e:
        return e


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_valid_command_name():
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
        return True

    @one.command
    def b():
        return False

    @two.command
    def x():
        return True

    @two.command
    def y():
        return False

    # Act.
    cx_a = execute(with_='one a')
    cx_b = execute(with_='one b')
    cx_x = execute(with_='two x')
    cx_y = execute(with_='two y')

    # Assert.
    assert cx_a is True
    assert cx_b is False
    assert cx_x is True
    assert cx_y is False


def test_invalid_command_name():
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

    @one.command
    def b():
        pass

    @two.command
    def x():
        pass

    @two.command
    def y():
        pass

    # Act.
    cx_a = execute(with_='three')
    cx_b = execute(with_='one c')
    cx_c = execute(with_='two z')
    cx_d = execute(with_='one x')
    cx_e = execute(with_='two a')

    # Assert.
    assert isinstance(cx_a, SystemExit)
    assert isinstance(cx_b, SystemExit)
    assert isinstance(cx_c, SystemExit)
    assert isinstance(cx_d, SystemExit)
    assert isinstance(cx_e, SystemExit)


def test_multiple_subcommands():
    # Arrange.
    @cli
    def main(debug: Flag):
        pass

    @main.command
    def first(x: Arg[int]):
        pass

    @first.command
    def second(y: Opt[int]):
        pass

    @second.command
    def third(z: Flag):
        return z

    # Act.
    cx = execute(with_='--debug first 1 second --y 2 third --z')

    # Assert.
    assert cx is True


def test_one_command_without_arguments():
    # Arrange.
    @cli
    def main():
        pass

    @main.command
    def sub():
        return True

    # Act.
    cx = execute(with_='sub')

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
    cx = execute(with_='sub 1 --y 2 --z')

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
    cx_a = execute(with_='one')
    cx_b = execute(with_='two')

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
    cx_a = execute(with_='one 1 --y 2 --z')
    cx_b = execute(with_='two 1 --y 2 --z')

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
    cx_a = execute(with_='one 1 --y 2 --z')
    cx_b = execute(with_='two 1 --b 2 --c')

    # Assert.
    assert cx_a == (+1, +2, True)
    assert cx_b == (-1, -2, True)
