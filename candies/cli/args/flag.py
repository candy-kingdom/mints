class Flag:
    """A command line argument that represents a boolean flag.

    Flag arguments are used to represent a turned on or turned off behaviour.
    Unlike positional arguments, they're prefixed with either short (`-`, `+`,
    `/`) or long (`--`, `++`, etc.) prefix, and can be used in any place of a
    call.

    For example, in the following line:

        $ git status --short

    `--short` is a flag that tells `status` command to print the output
    in the short-format.

    Attributes:
        description: A description of a flag. Shown in the help page.
        short: A short form of a flag.
            Must be non empty and consist of 1 alphabet character.
        prefix: A string that represents a prefix of a flag.
            It should contain only 1 character.
            For example, a value of `+` allows `++flag` and `+f` notation.
            Default is '-'.

    Examples:
        # To handle the mentioned above CLI, one could write:
        @cli
        def git():
            ...

        @git.command
        def status(short: Flag('Give the output in the short-format')):
            ...
    """

    def __init__(self, description: str = None, short: str = None, prefix = '-'):
        self.description = description
        self.short = short
        self.prefix = prefix
