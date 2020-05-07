from unittest.mock import MagicMock

from candies.cli.cli import cli, CLI
from candies.cli.parsers.parser import Invocation


def test_that_cli_decorates_function():
    def main():
        pass

    assert isinstance(cli(main), CLI)


def test_that_cli_returns_decorator_when_called_without_function():
    def main():
        pass

    decorator = cli()

    assert callable(decorator)
    assert isinstance(decorator(main), CLI)


def test_that_cli_calls_decorated_function():
    command = MagicMock()
    parser = MagicMock()
    parser.parse.return_value = [Invocation(args={'a': 'x', 'b': 42})]

    cli_ = CLI(command, parser)
    cli_(['a=x', 'b=42'])

    parser.parse.assert_called_once_with(['a=x', 'b=42'])
    command.func.assert_called_once_with(a='x', b=42)
