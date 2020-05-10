from typing import Callable, Any, List

from candies.cli.args.arg import Arg
from candies.cli.args.opt import Opt
from candies.cli.cli import cli


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
