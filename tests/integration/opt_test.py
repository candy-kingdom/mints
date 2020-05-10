"""Various tests for `candies.cli.args.opt.Opt`."""

from typing import Callable

from candies.cli.cli import cli
from candies.cli.args.arg import Arg
from candies.cli.args.opt import Opt
from candies.cli.args.flag import Flag


def execute(cli_: Callable, with_: str):
    try:
        return cli_(with_.split())
    # `BaseException`, because `argparse` calls `exit` on error.
    except BaseException as e:
        return e


def test_one_opt():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    cx = execute(main, with_='--x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_description():
    # Arrange.
    @cli
    def main(x: Opt('Description.')):
        return x

    # Act.
    cx = execute(main, with_='--x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_default_value():
    # Arrange.
    @cli
    def main(x: Opt = '2'):
        return x

    # Act.
    cx = execute(main, with_='--x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_default_value_but_not_specified_in_cli():
    # Arrange.
    @cli
    def main(x: Opt = '2'):
        return x

    # Act.
    cx = execute(main, with_='')

    # Assert.
    assert cx == '2'


def test_one_opt_not_specified_in_cli():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    ex = execute(main, with_='')

    # Assert.
    assert isinstance(ex, BaseException)


def test_one_opt_with_default_value_but_different_opt_specified_in_cli():
    # Arrange.
    @cli
    def main(x: Opt = '2'):
        return x

    # Act.
    ex = execute(main, with_='--y 1')

    # Assert.
    assert isinstance(ex, BaseException)


def test_one_opt_without_value():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    ex = execute(main, with_='--x')

    # Assert.
    assert isinstance(ex, BaseException)


def test_two_opts():
    # Arrange.
    @cli
    def main(x: Opt, y: Opt):
        return x, y

    # Act.
    cx = execute(main, with_='--x 1 --y 2')

    # Assert.
    assert cx == ('1', '2')


def test_two_opts_in_different_order():
    # Arrange.
    @cli
    def main(x: Opt, y: Opt):
        return x, y

    # Act.
    cx = execute(main, with_='--y 2 --x 1')

    # Assert.
    assert cx == ('1', '2')


def test_one_opt_before_flag():
    # Arrange.
    @cli
    def main(x: Opt, y: Flag):
        return x, y

    # Act.
    cx = execute(main, with_='--x 1 --y')

    # Assert.
    assert cx == ('1', True)


def test_one_opt_before_arg():
    # Arrange.
    @cli
    def main(x: Opt, y: Arg):
        return x, y

    # Act.
    cx = execute(main, with_='--x 1 2')

    # Assert.
    assert cx == ('1', '2')


def test_one_opt_specified_without_value_but_another_flag():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    ex = execute(main, with_='--x --y')

    # Assert.
    assert isinstance(ex, BaseException)


def test_one_opt_with_implicit_short():
    # Arrange.
    @cli
    def main(xyz: Opt):
        return xyz

    # Act.
    cx = execute(main, with_='-x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_explicit_short():
    # Arrange.
    @cli
    def main(x: Opt(short='y')):
        return x

    # Act.
    cx = execute(main, with_='-y 1')

    # Assert.
    assert cx == '1'


def test_opt_specified_twice():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    cx = execute(main, with_='--x 1 --x 2')

    # Assert.
    assert cx == '2'
