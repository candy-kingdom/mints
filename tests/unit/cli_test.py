from unittest.mock import MagicMock

from candies.cli import cli, CLI


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
    func = MagicMock()
    parser = MagicMock()
    parser.parse.return_value = {'a': 'x', 'b': 42}

    cli_ = CLI(func)
    cli_(['a=x', 'b=42'], parser)

    parser.parse.assert_called_once_with(['a=x', 'b=42'])
    func.assert_called_once_with(a='x', b=42)
