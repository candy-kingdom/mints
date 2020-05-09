class Opt:
    """A command line argument that represents an option.

    Options are used to represent named arguments.
    Like flags (`Flag`), they have either short (`-`, `+`, `/`)
    or long (`--`, `++`, etc.) prefix, and can be used in any place of a call.
    Like arguments (`Arg`), options have values.

    For example, in the following line:

        $ say "Hello, world!" --times 3

    `--times` is an option with value of `3`.

    Attributes:
        description (str): A description of an argument. Shown in help page.
        short (str): A short form of an argument.
            Must be non empty and consist of 1 alphabetic letter.

    Examples:
        # To handle the mentioned above CLI, one could write:
        @cli
        def git():
            ...

        @git.command
        def status(short: Flag('Give the output in the short-format')):
            ...
    """

    def __init__(self, description: str = None, short: str = None):
        self.description = description
        self.short = short
