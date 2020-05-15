"""Various tests for `candies.cli.args.flag.Flag`."""

from typing import Any
from argparse import ArgumentError

import pytest

from candies.cli.cli import cli, CLI
from candies.cli.args.flag import Flag
from candies.cli.args.arg import Arg

from tests.execution import execute, redirect_stderr


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_one_flag():
    # Arrange.
    @cli
    def main(x: Flag):
        return x

    # Act.
    cx = execute(cli, '--x')

    # Assert.
    assert cx == True


def test_one_flag_with_description():
    # Arrange.
    @cli
    def main(x: Flag('Description.')):
        return x

    # Act.
    cx = execute(cli, '--x')

    # Assert.
    assert cx == True


def test_one_flag_with_default_false():
    # Arrange.
    @cli
    def main(x: Flag = False):
        return x

    # Act.
    cx = execute(cli, '--x')

    # Assert.
    assert cx == True


def test_one_flag_with_default_true():
    # Arrange.
    @cli
    def main(x: Flag = True):
        return x

    # Act.
    cx = execute(cli, '--x')

    # Assert.
    assert cx == True


def test_one_flag_with_default_int():
    # Arrange.
    @cli
    def main(x: Flag = 5):
        return x

    # Act.
    ex = execute(cli, '--x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert 'Expected a `bool`' in str(ex)


def test_one_flag_not_specified():
    # Arrange.
    @cli
    def main(x: Flag):
        return x

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == False


def test_one_flag_not_specified_with_default_false():
    # Arrange.
    @cli
    def main(x: Flag = False):
        return x

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == False


def test_one_flag_not_specified_with_default_true():
    # Arrange.
    @cli
    def main(x: Flag = True):
        return x

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == True


def test_two_flags():
    # Arrange.
    @cli
    def main(x: Flag, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '--x --y')

    # Assert.
    assert cx == (True, True)


def test_two_flags_in_different_order():
    # Arrange.
    @cli
    def main(x: Flag, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '--y --x')

    # Assert.
    assert cx == (True, True)


def test_two_flags_one_specified():
    # Arrange.
    @cli
    def main(x: Flag, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '--x')

    # Assert.
    assert cx == (True, False)


def test_two_flags_not_specified():
    # Arrange.
    @cli
    def main(x: Flag, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == (False, False)


def test_one_flag_after_arg():
    # Arrange.
    @cli
    def main(x: Arg, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '1 --y')

    # Assert.
    assert cx == ('1', True)


def test_one_flag_before_arg():
    # Arrange.
    @cli
    def main(x: Arg, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '--y 1')

    # Assert.
    assert cx == ('1', True)


def test_one_arg_between_two_flags():
    # Arrange.
    @cli
    def main(x: Arg, y: Flag, z: Flag):
        return x, y, z

    # Act.
    cx = execute(cli, '--y 1 --z')

    # Assert.
    assert cx == ('1', True, True)


def test_one_arg_with_flag_not_specified():
    # Arrange.
    @cli
    def main(x: Arg, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '1')

    # Assert.
    assert cx == ('1', False)


def test_one_flag_without_short():
    # Arrange.
    @cli
    def main(xyz: Flag):
        return xyz

    # Act.
    ex, err = execute(cli, '-x', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'unrecognized arguments: -x' in err


def test_one_flag_with_explicit_short():
    # Arrange.
    @cli
    def main(xyz: Flag(short='a')):
        return xyz

    # Act.
    cx = execute(cli, '-a')

    # Assert.
    assert cx == True


def test_one_flag_with_explicit_short_and_description():
    # Arrange.
    @cli
    def main(xyz: Flag('Description.', short='a')):
        return xyz

    # Act.
    cx = execute(cli, '-a')

    # Assert.
    assert cx == True


def test_two_flags_with_same_implicit_shorts():
    # Arrange.
    @cli
    def main(xy: Flag, xz: Flag):
        return xy, xz

    # Act.
    cx = execute(cli, '--xy --xz')

    # Assert.
    assert cx == (True, True)


def test_two_flags_with_same_explicit_shorts():
    # Arrange.
    @cli
    def main(x: Flag(short='a'), y: Flag(short='a')):
        return x, y

    # Act.
    ex = execute(cli, '--x --y')

    # Assert.
    assert isinstance(ex, ArgumentError)
    assert 'conflicting option string: -a' in str(ex)


def test_flag_with_empty_short():
    # Arrange.
    @cli
    def main(x: Flag(short='')):
        return x

    # Act.
    ex = execute(cli, '--x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid short name '': it is an empty" in str(ex)


def test_flag_with_too_long_short():
    # Arrange.
    @cli
    def main(x: Flag(short='ab')):
        return x

    # Act.
    ex = execute(cli, '--x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid short name 'ab': it consists of more than one" in str(ex)


def test_flag_with_digit_short():
    # Arrange.
    @cli
    def main(x: Flag(short='1')):
        return x

    # Act.
    ex = execute(cli, '--x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid short name '1': it is not an alphabet" in str(ex)


def test_flag_with_sign_short():
    # Arrange.
    @cli
    def main(x: Flag(short='-')):
        return x

    # Act.
    ex = execute(cli, '--x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid short name '-': it is not an alphabet" in str(ex)


def test_flag_specified_twice():
    # Arrange.
    @cli
    def main(x: Flag):
        return x

    # Act.
    cx = execute(cli, '--x --x')

    # Assert.
    assert cx is True


def test_flag_with_custom_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='+')):
        return x

    # Act.
    cx = execute(cli, '++x')

    # Assert.
    assert cx == True


def test_flag_with_custom_prefix_and_short():
    # Arrange.
    @cli
    def main(xyz: Flag(short='x', prefix='+')):
        return xyz

    # Act.
    cx = execute(cli, '+x')

    # Assert.
    assert cx is True


def test_flag_with_custom_but_default_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='-')):
        return x

    # Act.
    cx = execute(cli, '--x')

    # Assert.
    assert cx == True


def test_flag_with_letter_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='a')):
        return x

    # Act.
    cx = execute(cli, 'aax')

    # Assert.
    assert cx is True


def test_flag_with_empty_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='')):
        return x

    # Act.
    ex = execute(cli, 'x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid prefix '': it is an empty" in str(ex)


def test_flag_with_none_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix=None)):
        return x

    # Act.
    ex = execute(cli, 'x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid prefix 'None': it is None" in str(ex)


def test_flag_with_long_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='--')):
        return x

    # Act.
    ex = execute(cli, '----x')

    # Assert.
    assert isinstance(ex, ValueError)
    assert "'x' has an invalid prefix '--': it consists of more than one" in str(ex)


def test_flag_specified_with_wrong_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='+')):
        return x

    # Act.
    ex, err = execute(cli, '--x', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'unrecognized arguments: --x' in err


def test_flag_with_non_string_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix=[1])):
        return x

    # Act.
    ex = execute(cli, '--x')

    # Assert.
    assert isinstance(ex, TypeError)
    assert "unhashable type: 'list'" in str(ex)


def test_two_flags_and_one_with_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='+'), y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '++x --y')

    # Assert.
    assert cx == (True, True)


def test_two_flags_with_same_prefix():
    # Arrange.
    @cli
    def main(x: Flag(prefix='+'), y: Flag(prefix='+')):
        return x, y

    # Act.
    cx = execute(cli, '++x ++y')

    # Assert.
    assert cx == (True, True)


def test_flag_of_subcommand_with_custom_prefix():
    # Arrange.
    @cli
    def main():
        ...

    @main.command
    def sub(x: Flag(prefix='+')):
        return x

    # Act.
    cx = execute(cli, 'sub ++x')

    # Assert.
    assert cx == True
