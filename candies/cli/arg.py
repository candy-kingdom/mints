class Arg:
    """An argument of a command line.

    Intended to be used as a type annotation in CLI functions to help
    the parser distinguish simple arguments, flags, prompts, etc.

    Note:
        Consider looking at the documentation of the `candies.cli.CLI` class
        for more details about which kinds of CLIs the `Arg` produces.

    Attributes:
        description (str): A description of an argument.

    Examples:
        @cli
        def main(a: Arg['argument a'],
                 b: Arg['argument b']):
            ...
    """

    def __init__(self, description: str = None):
        self.description = description

    def __class_getitem__(cls, description: str):
        return Arg(description)
