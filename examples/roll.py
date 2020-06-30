"""An example of a simple CLI for rolling dice.

The example demonstrates the usage of a typed argument
accepting a list of custom objects (instances of `Roll`).

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

from mints import cli, Arg


class Roll:
    """A roll of a die."""

    def __init__(self, sides: int, times: int):
        self._sides = sides
        self._times = times

    def __call__(self) -> List[int]:
        """Rolls the die the required number of times."""
        return [random.randint(1, self._sides) for _ in range(self._times)]


@cli
def roll(rolls: Arg[List[Roll]]('a list of dice rolls')):
    """Roll dice.

    Each die should be specified using the dice notation: [m]d{n},
    where `m` stands for the number of times to roll a die (optional),
    and `n` stands for the number of sides of a die.
    For example,
        - 2d6  means "roll two 6-sided dice",
        - 1d10 means "roll one 10-sided die",
        - d20  means "roll one 20-sided die".

    Usage examples:
        $ python roll.py 1d6
        3
        $ python roll.py 3d6 d20
        2 5 1
        17
    """

    if not rolls:
        exit('You should specify at least a single die roll. \n'
             'See `--help` for usage examples.')

    for roll in rolls:
        print(' '.join(str(x) for x in roll()))


@cli.parse
def roll(x: str) -> Roll:
    """Parses a single die roll from the dice notation."""

    pattern = re.compile(r'(?P<times>\d*)d(?P<sides>\d+)')

    if not (match := pattern.match(x)):
        exit(f'A die roll was specified in an invalid format: "{x}". \n'
             f'See `--help` for usage examples.')

    group = match.groupdict()
    times = int(group['times'] or '1')
    sides = int(group['sides'])

    if sides == 0:
        exit('Really? A zero-sided die?')

    return Roll(sides, times)


if __name__ == '__main__':
    cli()
