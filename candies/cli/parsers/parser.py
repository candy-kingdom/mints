from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any


class Parser(metaclass=ABCMeta):
    """A parser for command line arguments."""

    @abstractmethod
    def parse(self, args: List[str]) -> Dict[str, Any]:
        """Parses the specified arguments.

        Args:
            args: A list of arguments as they would be presented in `argv`
                (except for the name of the file). For example, an input string
                'main.py --a=10 --b=20' should be converted to
                ['--a=10', '--b=20'] and passed to this method.

        Returns:
            A dictionary that maps names of arguments to their values.
            For example, an input ['--a=10', '--b=20'] may be parsed as
            {'a': '10', 'b': '20'}.
        """
