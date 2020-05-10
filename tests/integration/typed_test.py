from typing import Callable, Any, List

from candies.cli.args.arg import Arg
from candies.cli.args.opt import Opt
from candies.cli.cli import cli

import pytest


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


def execute(cli_: Callable, with_: str) -> Any:
    try:
        return cli_(with_.split())
    # `SystemExit`, because `argparse` calls `exit` on error.
    except SystemExit as e:
        return e


def test_typed_arg_without_description():
    # Arrange.
    @cli
    def main(x: Arg[int]):
        return x

    # Act.
    cx = execute(main, with_='10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_arg_with_description():
    # Arrange.
    @cli
    def main(x: Arg[int]('Description.')):
        return x

    # Act.
    cx = execute(main, with_='10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_arg_with_invalid_value():
    # Arrange.
    @cli
    def main(x: Arg[int]):
        return x

    # Act.
    cx = execute(main, with_='whatever')

    # Assert.
    assert isinstance(cx, SystemExit)


def test_typed_opt_without_description():
    # Arrange.
    @cli
    def main(x: Opt[int]):
        return x

    # Act.
    cx = execute(main, with_='--x 10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_typed_opt_with_description():
    # Arrange.
    @cli
    def main(x: Opt[int]('Description.')):
        return x

    # Act.
    cx = execute(main, with_='--x 10')

    # Assert.
    assert isinstance(cx, int)
    assert cx == 10


def test_args_typed_with_lists():
    # Arrange.
    @cli
    def main(x: Arg[int], y: Arg[List[int]], z: Arg[List[int]]):
        return x, y, z

    # Act.
    cx = execute(main, with_='1 2 3 4')

    # Assert.
    assert cx == (1, [2, 3, 4], [])


def test_opts_typed_with_lists():
    # Arrange.
    @cli
    def main(x: Opt[int], y: Opt[List[int]], z: Opt[int]):
        return x, y, z

    # Act.
    cx = execute(main, with_='--x 1 --y 2 3 4 --z 5')

    # Assert.
    assert cx == (1, [2, 3, 4], 5)


def test_args_and_opts_typed_with_lists():
    # Arrange.
    @cli
    def main(x: Arg[int], y: Arg[List[int]], z: Opt[List[int]]):
        return x, y, z

    # Act.
    cx = execute(main, with_='1 2 3 --z 4 5')

    # Assert.
    assert cx == (1, [2, 3], [4, 5])


def test_arg_typed_with_custom_type():
    # Arrange.
    @cli
    def main(add: Opt[Money]):
        return add

    @main.parse
    def money(x: str) -> Money:
        if x.startswith('$'):
            return Money.dollars(float(x[1:]))

    # Act.
    cx = execute(main, with_='--add $500')

    # Assert.
    assert cx == Money(500, 'dollars')


def test_arg_typed_with_list_of_custom_type():
    # Arrange.
    @cli
    def main(add: Opt[List[Money]]):
        return add

    @main.parse
    def money(x: str) -> Money:
        if x.startswith('$'):
            return Money.dollars(float(x[1:]))

    # Act.
    cx = execute(main, with_='--add $100 $200')

    # Assert.
    assert cx == [Money(100, 'dollars'), Money(200, 'dollars')]


def test_arg_typed_with_unsupported_type():
    # Arrange.
    @cli
    def main(add: Opt[Money]):
        return add

    # Act.
    cx = execute(main, with_='--add $500')

    # Assert.
    assert isinstance(cx, BaseException)


def test_arg_typed_with_list_of_unsupported_types():
    # Arrange.
    @cli
    def main(add: Opt[List[Money]]):
        return add

    # Act.
    cx = execute(main, with_='--add $100 $200')

    # Assert.
    assert isinstance(cx, BaseException)


def test_parse_with_unannotated_parser_function():
    # Arrange.
    @cli
    def main():
        pass

    # Act & Assert.
    with pytest.raises(ValueError):
        @main.parse
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
    @main.parse
    def a(x: str) -> Example:
        pass

    with pytest.raises(ValueError, match="namely 'a'"):
        @main.parse
        def b(x: str) -> Example:
            pass
