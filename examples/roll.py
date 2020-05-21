"""An example of a simple CLI for rolling dice.

The example demonstrates a usage of a typed argument
accepting a list of custom objects (instances of `Die`).

Usage:
    $ python roll.py 1d6
    3
    $ python roll.py 2d6
    2 5
    $ python roll.py 1d6 2d3
    6
    2 1
"""

import re
import random
from typing import List

from candies.cli import cli, Arg


class Die:
    """Represents a die to roll."""

    def __init__(self, sides: int, rolls: int):
        self._sides = sides
        self._rolls = rolls

    def roll(self) -> List[int]:
        """Rolls the die the required amount of times."""
        return [random.randint(1, self._sides) for _ in range(self._rolls)]


@cli
def roll(dice: Arg[List[Die]]('A list of dice to roll.')):
    """Roll dice.

    A list of dice should be specified using the dice notation: [m]d{n}.
    For example,
        - 2d6  means "roll 2 6-sided dice",
        - 1d10 means "roll 1 10-sided die",
        - d20  means "roll 1 20-sided die".
    """

    if not dice:
        exit('Try specifying at least a single die to roll.')

    for die in dice:
        print(' '.join(map(str, die.roll())))


@cli.parse
def die(x: str) -> Die:
    """Parses a die from the dice notation [m]d{n}."""

    pattern = re.compile(r'(?P<rolls>\d*)d(?P<sides>\d+)')

    if not (match := pattern.match(x)):
        exit(f'A die was specified in an invalid format: "{x}". \n'
             f'Try something like "2d6" or "d20".')

    group = match.groupdict()
    rolls = int(group['rolls'] or '1')
    sides = int(group['sides'])

    if sides == 0:
        exit('Really? A zero-sided die?')

    return Die(sides, rolls)


if __name__ == '__main__':
    cli()
