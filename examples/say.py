"""An example CLI to print a phrase.

This example demonstrates a simple usage of typed positional
and optional arguments, as well as flags and default values.

Usage:
    $ python say.py Hello!
    Hello!
    $ python say.py Hello! --times 2
    Hello!
    Hello!
    $ python say.py Hello! --times 3 --caps
    HELLO!
    HELLO!
    HELLO!
"""

from mints import cli, Arg, Opt, Flag


@cli
def say(phrase: Arg('a phrase to print'),
        caps:   Flag('whether to print in the upper-case'),
        times:  Opt[int]('how many times to print') = 1):
    """Prints a phrase specified number of times."""

    for _ in range(times):
        print(phrase.upper() if caps else phrase)


if __name__ == '__main__':
    cli()
