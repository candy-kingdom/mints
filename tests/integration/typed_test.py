"""Various tests for `candies.cli.args.typed.Typed`."""

from typing import Any, List

import pytest

from mints.args.arg import Arg
from mints.args.opt import Opt
from mints.cli import cli, CLI

from tests.execution import execute, redirect_stderr


class Money:
    def __init__(self, value: float, currency: str):
        self.value = value
        self.currency = currency

    def __eq__(self, other):
        return isinstance(other, Money) \
               and self.value == other.value \
               and self.currency == other.currency

    @staticmethod
    def dollars(value: float):
        return Money(value, 'dollars')


@pytest.fixture(autouse=True)
def reset():
    # Reset `cli` before each test
    # as if we have just imported it.
    globals()['cli'] = CLI()


def test_typed_arg_without_description():
    # Arrange.
    @cli
    def main(x: Arg[int]):
        return x

    # Act.
    cx = execute(cli, '10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_arg_with_description():
    # Arrange.
    @cli
    def main(x: Arg[int]('Description.')):
        return x

    # Act.
    cx = execute(cli, '10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_arg_with_invalid_value():
    # Arrange.
    @cli
    def main(x: Arg[int]):
        return x

    # Act.
    cx, err = execute(cli, 'a', redirect_stderr)

    # Assert.
    assert isinstance(cx, SystemExit)
    assert 'invalid int value' in err



def test_typed_opt_without_description():
    # Arrange.
    @cli
    def main(x: Opt[int]):
        return x

    # Act.
    cx = execute(cli, '--x 10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_opt_with_description():
    # Arrange.
    @cli
    def main(x: Opt[int]('Description.')):
        return x

    # Act.
    cx = execute(cli, '--x 10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_args_typed_with_lists():
    # Arrange.
    @cli
    def main(x: Arg[int], y: Arg[List[int]], z: Arg[List[int]]):
        return x, y, z

    # Act.
    cx = execute(cli, '1 2 3 4')

    # Assert.
    assert cx == (1, [2, 3, 4], [])


def test_opts_typed_with_lists():
    # Arrange.
    @cli
    def main(x: Opt[int], y: Opt[List[int]], z: Opt[int]):
        return x, y, z

    # Act.
    cx = execute(cli, '--x 1 --y 2 3 4 --z 5')

    # Assert.
    assert cx == (1, [2, 3, 4], 5)


def test_args_and_opts_typed_with_lists():
    # Arrange.
    @cli
    def main(x: Arg[int], y: Arg[List[int]], z: Opt[List[int]]):
        return x, y, z

    # Act.
    cx = execute(cli, '1 2 3 --z 4 5')

    # Assert.
    assert cx == (1, [2, 3], [4, 5])


def test_arg_typed_with_custom_type():
    # Arrange.
    @cli
    def main(add: Opt[Money]):
        return add

    @cli.parse
    def money(x: str) -> Money:
        if x.startswith('$'):
            return Money.dollars(float(x[1:]))

    # Act.
    cx = execute(cli, '--add $500')

    # Assert.
    assert cx == Money(500, 'dollars')


def test_arg_typed_with_list_of_custom_type():
    # Arrange.
    @cli
    def main(add: Opt[List[Money]]):
        return add

    @cli.parse
    def money(x: str) -> Money:
        if x.startswith('$'):
            return Money.dollars(float(x[1:]))

    # Act.
    cx = execute(cli, '--add $100 $200')

    # Assert.
    assert cx == [Money(100, 'dollars'), Money(200, 'dollars')]


def test_arg_typed_with_unsupported_type():
    # Arrange.
    @cli
    def main(add: Opt[Money]):
        return add

    # Act.
    cx, err = execute(cli, '--add $500', redirect_stderr)

    # Assert.
    assert isinstance(cx, SystemExit)
    assert 'invalid Money value' in err


def test_arg_typed_with_list_of_unsupported_types():
    # Arrange.
    @cli
    def main(add: Opt[List[Money]]):
        return add

    # Act.
    cx, err = execute(cli, '--add $100 $200', redirect_stderr)

    # Assert.
    assert isinstance(cx, SystemExit)
    assert 'invalid Money value' in err


def test_parse_with_unannotated_parser_function():
    # Arrange.
    @cli
    def main():
        pass

    # Act & Assert.
    with pytest.raises(ValueError):
        @cli.parse
        def something(x: str):
            pass


def test_parse_with_duplicate_parser_function():
    # Arrange.
    @cli
    def main():
        pass

    class Example:
        pass

    # Act & Assert.
    @cli.parse
    def a(x: str) -> Example:
        pass

    with pytest.raises(ValueError, match="namely 'a'"):
        @cli.parse
        def b(x: str) -> Example:
            pass


def test_add_parser_with_type():
    # Arrange.
    class Example:
        def __init__(self, value: Any):
            self.value = value

        def __eq__(self, other):
            return isinstance(other, Example) and self.value == other.value

    @cli
    def main(x: Arg[Example]):
        return x

    cli.add_parser(Example)

    # Act.
    cx = execute(cli, '10')

    # Assert.
    assert cx == Example('10')


def test_add_parser_with_duplicate_type():
    # Arrange.
    class Example:
        def __init__(self, value: Any):
            self.value = value

        def __eq__(self, other):
            return isinstance(other, Example) and self.value == other.value

    @cli
    def main(x: Arg[Example]):
        return x

    # Act & Assert.
    cli.add_parser(Example)

    with pytest.raises(ValueError, match="namely 'Example'"):
        cli.add_parser(Example)
