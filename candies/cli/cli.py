"""
    TODO: Description.
"""


def cli(func=None):
    """Constructs a CLI from the specified function."""

    if func is None:
        return \
            lambda x: CLI(x)
    else:
        return CLI(func)


class CLI:
    """TODO."""

    def __init__(self, main):
        self._main = main

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def command(self, func):
        raise NotImplementedError
