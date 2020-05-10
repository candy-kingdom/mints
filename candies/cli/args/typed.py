from typing import Type, Any


class Typed:
    """A typed command line argument.

    A typed command line argument is used for specifying the type
    to convert the value to. For example, consider the following code:

        @cli
        def double(number: Opt[int]('A number to double.')):
            print(number * 2)

    When this CLI is called as

        $ example.py double --number 5

    the value '5' of the argument '--number' is converted to `int`
    and passed to the function.

    Note:
        The default type of arguments is `str`. Thus, if an argument
        is annotated as `Opt('A number to double.')`, a string value
        will be passed to the function.

    Attributes:
        kind: A kind of an argument
            (for example, `Arg`, `Opt` or `Flag`).
        type: A type of an argument
            (for example, `int`, `List[double]`, etc.).
    """

    def __init__(self, kind: Type, type: Type):
        self.kind = kind
        self.type = type

    def __call__(self, *args: Any, **kwargs: Any) -> 'Typed':
        # Instantiate the parameter being wrapped. For example,
        # `Arg[int]` will return `Typed(Arg, int)`, and
        # `Typed(Arg, int)('Description.')` will instantiate
        # `self.kind = Arg('Description.')`.
        if isinstance(self.kind, type):
            self.kind = self.kind(*args, **kwargs)
        else:
            raise ValueError(f"Cannot instantiate {type(self.kind)} twice: it"
                             f"is already instantiated as {repr(self.kind)}.")

        return self
