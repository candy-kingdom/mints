from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any


class Parser(metaclass=ABCMeta):
    """A parser for command line arguments."""

    @abstractmethod
    def parse(self, args: List[str]) -> Dict[str, Any]:
        """Parses the specified arguments."""
