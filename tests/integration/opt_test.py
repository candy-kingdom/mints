"""Various tests for `mints.args.opt.Opt`.

Consider looking at `tests.integration.flag_test` for more details about some
specific behaviour that is shared between flags and options.
"""

import pytest

from mints.cli import cli, CLI
from mints.args.arg import Arg
from mints.args.opt import Opt
from mints.args.flag import Flag

from tests.execution import execute, redirect_stderr


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_one_opt():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    cx = execute(cli, '--x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_description():
    # Arrange.
    @cli
    def main(x: Opt('Description.')):
        return x

    # Act.
    cx = execute(cli, '--x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_default_value():
    # Arrange.
    @cli
    def main(x: Opt = '2'):
        return x

    # Act.
    cx = execute(cli, '--x 1')

    # Assert.
    assert cx == '1'


def test_one_opt_with_default_value_but_not_specified_in_cli():
    # Arrange.
    @cli
    def main(x: Opt = '2'):
        return x

    # Act.
    cx = execute(cli, '')

    # Assert.
    assert cx == '2'


def test_one_opt_not_specified_in_cli():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    ex, err = execute(cli, '', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'required: --x' in err


def test_one_opt_with_default_value_but_different_opt_specified_in_cli():
    # Arrange.
    @cli
    def main(x: Opt = '2'):
        return x

    # Act.
    ex, err = execute(cli, '--y 1', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'unrecognized arguments: --y 1' in err


def test_one_opt_without_value():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    ex, err = execute(cli, '--x', redirect_stderr)

    # Assert.
    assert isinstance(ex, BaseException)
    assert 'argument --x: expected one argument' in err


def test_two_opts():
    # Arrange.
    @cli
    def main(x: Opt, y: Opt):
        return x, y

    # Act.
    cx = execute(cli, '--x 1 --y 2')

    # Assert.
    assert cx == ('1', '2')


def test_two_opts_in_different_order():
    # Arrange.
    @cli
    def main(x: Opt, y: Opt):
        return x, y

    # Act.
    cx = execute(cli, '--y 2 --x 1')

    # Assert.
    assert cx == ('1', '2')


def test_one_opt_before_flag():
    # Arrange.
    @cli
    def main(x: Opt, y: Flag):
        return x, y

    # Act.
    cx = execute(cli, '--x 1 --y')

    # Assert.
    assert cx == ('1', True)


def test_one_opt_before_arg():
    # Arrange.
    @cli
    def main(x: Opt, y: Arg):
        return x, y

    # Act.
    cx = execute(cli, '--x 1 2')

    # Assert.
    assert cx == ('1', '2')


def test_one_opt_specified_without_value_but_another_flag():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    ex, err = execute(cli, '--x --y', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert '--x: expected one argument' in err


def test_one_opt_with_implicit_short():
    # Arrange.
    @cli
    def main(xyz: Opt):
        return xyz

    # Act.
    ex, err = execute(cli, '-x 1', redirect_stderr)

    # Assert.
    assert isinstance(ex, SystemExit)
    assert 'required: --xyz' in err


def test_one_opt_with_explicit_short():
    # Arrange.
    @cli
    def main(x: Opt(short='y')):
        return x

    # Act.
    cx = execute(cli, '-y 1')

    # Assert.
    assert cx == '1'


def test_opt_specified_twice():
    # Arrange.
    @cli
    def main(x: Opt):
        return x

    # Act.
    cx = execute(cli, '--x 1 --x 2')

    # Assert.
    assert cx == '2'


def test_opt_with_custom_prefix():
    # Arrange.
    @cli
    def main(x: Opt(prefix='+')):
        return x

    # Act.
    cx = execute(cli, '++x 1')

    # Assert.
    assert cx == '1'
