# {Name}

[![Build](https://github.com/candy-kingdom/cli/workflows/Build/badge.svg)](https://github.com/JoshuaLight/chalice-restful/actions)

_Clean and elegant CLI development kit._

## Overview

{Name} is a microframework that allows building declarative and nice-looking CLI apps.

Consider the following example as a demonstration of {Name} capabilities:
```py
# say.py

from {pyname} import cli, Arg, Flag, Opt

@cli
def say(phrase: Arg('a phrase to print'),
        caps:   Flag('whether to print phrase in upper-case'),
        times:  Opt[int]('how many times to print') = 1):
    """Prints a phrase specified number of times."""

    for i in range(0, times):
        print(phrase.upper() if caps else phrase)


if __name__ == '__main__':
    cli()
```

It then can be used as follows:
```
$ python3 say.py "Hi!" 
Hi!
$ python3 say.py "Hi!" --caps
HI!
$ python3 say.py "Hi!" --times 3
Hi!
Hi!
Hi!
$ python3 say.py --help
usage: say [-h] [--caps] [--times TIMES] phrase

Prints a phrase specified number of times.

positional arguments:
  phrase         a phrase to print

optional arguments:
  -h, --help     show this help message and exit
  --caps         whether to print phrase in upper-case
  --times TIMES  how many times to print
```

## Install

```
$ pip install {pipname}
```

## Getting started

In general, writing a CLI app is very similar to writing a regular function.
{Name} is based on this metaphor, allowing to describe the whole interface of the app using only a function signature.
Consider the following example:
```py
# print.py

from {pyname} import cli, Arg

@cli
def entry(phrase: Arg):
    print(phrase)


if __name__ == '__main__':
    cli()
```

The script can be executed as a command line app:
```
$ python3 print.py "Hello, world!"
Hello, world!
```

The main idea is very simple: you use the `cli` decorator to wrap a function that acts as an entry point of the application (`entry`), and then use the `cli()` to make things running.
`Arg` is used to annotate positional arguments of the CLI.

In the following section we'll discuss more deeply how to implement different types of parameters in {Name}.

### Parameters

There are three different type annotations that could be used to represent positional arguments, flags and options.

#### `Arg`

`Arg` is a type annotation for positional arguments.
In CLI, positional arguments work in same way as in programming languages.

Consider this function:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(x: Arg, y: Arg):
    print(x, y)


if __name__ == '__main__':
    cli()
```

It allows the following call in shell:
```
$ python test.py 1 2
(1, 2)
```

But not:
```
$ python test.py 1
```

It's possible though to add a default value for an argument:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(x: Arg, y: Arg = 2):
    print(some)


if __name__ == '__main__':
    cli()
```

To support the following:
```
$ python test.py 1
(1, 2)
```

Note: it's not possible to define something like this:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(x: Arg = 1, y: Arg):
    print(some)


if __name__ == '__main__':
    cli()
```

The function signature is not supported even in Python.

#### `Flag`

`Flag` is a type annotation for flags.
In CLI, flags are boolean arguments that represent a turned off or turned on behaviour.
Unlike positional ones, they could be specified in a command line only with special syntax.

For example, the following function signature:
```py
# test.py

from {pyname} import cli, Flag


@cli
def entry(some: Flag):
    print(some)


if __name__ == '__main__':
    cli()
```

Could be called from the command line as follows:
```
$ python test.py --some
True
```

But it's also possible to invoke the CLI without the flag:
```
$ python test.py
False
```

Flags also support default values, but that doesn't make much sense.
Default value of `False` is already set implicitly for each flag.
Default value of `True` makes a flag to be always true.

For example, one could define:
```py
# test.py

from {pyname} import cli, Flag


@cli
def entry(some: Flag = True):
    print(some)


if __name__ == '__main__':
    cli()
```

But this makes the flag `some` useless:
```
$ python test.py --some
True
$ python test.py
True
```

#### `Opt`

`Flag` is a type annotation for options.
In CLI, options are simply named arguments or flags with values.

For example, the following function signature:
```py
# test.py

from {pyname} import cli, Opt


@cli
def entry(some: Opt):
    print(some)


if __name__ == '__main__':
    cli()
```

Could be called from the command line as follows:
```
$ python test.py --some 1
1
```

Note: unlike with flags, it's not possible to _not_ specify the option by default.
```
$ python test.py --some
usage: entry [-h] --some SOME
entry: error: the following arguments are required: --some
```

But it's possible to specify the default value for `Opt`:
```py
# test.py

from {pyname} import cli, Opt


@cli
def entry(some: Opt = 1):
    print(some)


if __name__ == '__main__':
    cli()
```

So it's now possible to call the script as follows:
```
$ python test.py
1
```

#### Help page

Each CLI in {Name} has a built-in help page, which is automatically generated.

For example, for the following function:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(some: Arg):
    print(some)


if __name__ == '__main__':
    cli()
```

It's possible to invoke the help page using the flag `--help`:
```
$ python test.py --help
usage: entry [-h] some 

positional arguments:
  some

optional arguments:
  -h, --help  show this help message and exit
```

Note the lack of the overall program description as well as the description of the `some` argument.

To override the program description, one could write a simple doc-comment for the CLI function:
To assign a description to an argument, the `description` parameter of the argument constructor type should be used.

Consider the following example as a demonstration of both possibilities:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(some: Arg('some argument')):
    """A simple demonstration program."""
    print(some)


if __name__ == '__main__':
    cli()
```

This produces a following help page:
```
$ python test.py --help
usage: entry [-h] some 

A simple demonstration program.

positional arguments:
  some        some argument

optional arguments:
  -h, --help  show this help message and exit
```

#### Short name

Usually, both flags and options come with a shortcut syntax.
For example, instead of writing:
```
$ python test.py --some 1
```

One could write:
```
$ python test.py -s 1
```

To define a shortcut letter for a flag or an option, the `short` parameter of either `Flag` or `Opt` annotations should be used:
```py
# test.py

from {pyname} import cli, Flag


@cli
def entry(some: Flag(short='s')):
    print(some)


if __name__ == '__main__':
    cli()
```

This allows invoking the CLI with the following syntax:
```
$ python test.py -s
True
```

#### Prefix

Flags and options are usually called with the `-` prefix (in short and long variations).
To override this behaviour, the `prefix` parameter of either `Flag` or `Opt` annotations should be used.

Consider the following example:
```py
# test.py

from {pyname} import cli, Flag


@cli
def entry(some: Flag(prefix='+')):
    print(some)


if __name__ == '__main__':
    cli()
```

Then the command line interface could be invoked as follows:
```
$ python test.py ++some
True
```

#### Types

By default, the value that comes from the CLI, if it's an `Opt` or an `Arg`, is of `str` type.

Consider the following example:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(some: Arg):
    print(type(some))


if __name__ == '__main__':
    cli()
```

If an integer value is passed to the command line, the following output is produced:
```
$ python test.py 1
<class 'str'>
```

To enforce the value to be an `int`, the following syntax should be used:
```py
# test.py

from {pyname} import cli, Arg


@cli
def entry(some: Arg[int]):
    print(type(some))


if __name__ == '__main__':
    cli()
```

This makes `some` to be an integer:
```
$ python test.py 1
<class 'int'>
```

But sometimes, a custom type should be parsed from a command line.
This could be done by defining a parser for one using the `parse` decorator:
```py
# test.py

from {pyname} import cli, Arg


class Custom:
    ...


@cli
def entry(some: Arg[Custom]):
    ...


@cli.parse
def custom(x: str) -> Custom:
    ...


if __name__ == '__main__':
    cli()
```

Note: it's possible to manually add a parser for a type using the `add_parser` function.
It works in same way as the `parse` decorator:
```py
# test.py

from {pyname} import cli, Arg


class Custom:
    def parse(x: str) -> 'Custom':
        ...

    ...


@cli
def entry(some: Arg[Custom]):
    ...


cli.add_parser(Custom.parse)

if __name__ == '__main__':
    cli()
```

### Commands

Complex command line interfaces like `git` have subcommands like `git status`, `git pull`, `git push`, etc.
These subcommands act as separate CLIs and, thus, are separate functions in {Name}.

Consider the following example as a fake `git` CLI:
```py
# git.py

from {pyname} import cli


@cli
def entry():
    ...

@entry.command
def pull():
    if rebase:
        print('pulling with rebase')
    else:
        print('pulling')


@entry.command
def push():
    print('pushing')


if __name__ == '__main__':
    cli()
```

This CLI could be invoked as follows:
```
$ python git.py pull
pulling
$ python git.py pull --rebase
pulling with rebase
$ python git.py push
pushing
```

Note: it's possible to have a deeper hierarchies of subcommands.
For example, the `dotnet` CLI tool could be called as [`dotnet tool install ...`](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install).

To mimic that in {Name}, the following structure should be used:
```py
# dotnet.py

from {pyname} import cli


@cli
def entry():
    ...


@entry.command
def tool():
    ...


@tool.command
def install():
    ...


if __name__ == '__main__':
    cli()
```

## Learn more

Learn more from concrete and real-life [examples](https://github.com/candy-kingdom/cli/blob/master/examples/).

## License

The package is licensed under the [MIT](https://github.com/candy-kingdom/cli/blob/master/LICENSE) license.

## Contributing

...
