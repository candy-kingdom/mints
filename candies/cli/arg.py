class Arg:
    """An argument of a command line.

    Args:
        description (str, optional): A description of an argument.
    """

    def __init__(self, description: str = None):
        self.description = description

    def __class_getitem__(cls, description: str):
        return Arg(description)
