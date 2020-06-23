# Mints

[![PyPI version](https://badge.fury.io/py/mints.svg)](https://badge.fury.io/py/mints)
[![Build](https://github.com/candy-kingdom/mints/workflows/Build/badge.svg)](https://github.com/candy-kingdom/mints/actions)

_Clean and elegant CLI development kit._

## Overview

Mints is a microframework that allows building declarative and nice-looking CLI apps.
Unlike [Click](https://click.palletsprojects.com/en/7.x/) or [Plac](https://micheles.github.io/plac/), it utilizes [function annotations](https://www.python.org/dev/peps/pep-3107/) more than [decorators](https://www.python.org/dev/peps/pep-0318/).

Here is a quick example:
```py
# say.py

from mints import cli, Arg, Flag, Opt

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

And what we get in the command line:
```
$ python3 say.py "Hi!" 
Hi!
```
```
$ python3 say.py "Hi!" --caps
HI!
```
```
$ python3 say.py "Hi!" --times 3
Hi!
Hi!
Hi!
```
```
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
$ pip install mints
```

## Getting started

_Note: the examples are not [PEP 8](https://www.python.org/dev/peps/pep-0008/#blank-lines) compatible: one blank line is used instead of two to separate top-level definitions._

In general, writing a CLI app is very similar to writing a regular function.
This is also true for Mints.

Consider the following example:
```py
# say.py

from mints import cli, Arg

@cli
def say(phrase: Arg):
    print(phrase)

if __name__ == '__main__':
    cli()
```

The script can be executed as a command-line app:
```
$ python3 say.py "Hello, world!"
Hello, world!
```

The main idea is very simple: you use the `cli` decorator to wrap a function that acts as an entry point of the application (`say` function from the example above), and then call the `cli()` to make things running.

In the next sections you'll find out how to build more complex apps in Mints.

### Parameters

#### `Arg`

`Arg` is an annotation for positional arguments.

Positional arguments in CLIs work in the same way as in programming languages.

Consider the following function:
```py
# test.py

from mints import cli, Arg

@cli
def test(x: Arg, y: Arg):
    print(x, y)

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1 2
1 2
```

Note: it's not possible to execute the script without an argument.
```
$ python test.py 1
usage: test [-h] x y
test: error: the following arguments are required: y
```

To address this issue, you could provide a default value to the argument:
```py
# test.py

from mints import cli, Arg

@cli
def test(x: Arg, y: Arg = 2):
    print(x, y)

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1
1 2
```

#### `Flag`

`Flag` is an annotation for flags.

Flags are boolean arguments that represent an on/off behavior.
Unlike positional arguments, they should be specified in the command line only with a special syntax.

Here is an example of a flag:
```py
# test.py

from mints import cli, Flag

@cli
def test(some: Flag):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py --some
True
```
```
$ python test.py
False
```

#### `Opt`

`Opt` is an annotation for options.

Options are simply flags with values (or arguments with names).

That's how you use the `Opt`:
```py
# test.py

from mints import cli, Opt

@cli
def test(some: Opt):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py --some 1
1
```

Note: it's not possible to _not_ specify the option by default, as it was for flags.
```
$ python test.py --some
usage: test [-h] --some SOME
test: error: the following arguments are required: --some
```

You still could provide a default value:
```py
# test.py

from mints import cli, Opt

@cli
def test(some: Opt = 1):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py
1
```

### Help page

Each CLI in Mints has a built-in help page, which is automatically generated.

Consider the following example:
```py
# test.py

from mints import cli, Arg

@cli
def test(some: Arg):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py --help
usage: test [-h] some 

positional arguments:
  some

optional arguments:
  -h, --help  show this help message and exit
```

Note the lack of the program description as well as the `some` argument description.

To override the description of the program, put a simple doc-comment to a CLI function.
To assign a description to an argument, instantiate an annotation with the `description` argument (it always comes first).

```py
# test.py

from mints import cli, Arg

@cli
def test(some: Arg('some argument')):
    """A simple demonstration program."""
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py --help
usage: test [-h] some 

A simple demonstration program.

positional arguments:
  some        some argument

optional arguments:
  -h, --help  show this help message and exit
```

### Short name

Usually, both flags and options come with a shortcut syntax.
For example, instead of writing:
```
$ python test.py --some 1
```

One could write:
```
$ python test.py -s 1
```

To define a shortcut letter for a flag or an option, the `short` parameter of either `Flag` or `Opt` should be used:
```py
# test.py

from mints import cli, Flag

@cli
def test(some: Flag(short='s')):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py -s
True
```

### Prefix

Flags and options are usually called with the `-` prefix (in short and long variations).
To override this behavior, the `prefix` parameter of either `Flag` or `Opt` should be used.
```py
# test.py

from mints import cli, Flag

@cli
def test(some: Flag(prefix='+')):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py ++some
True
```

### Types

By default, an argument that is passed from the CLI is of `str` type if it's annotated with either `Opt` or `Arg`, and of `bool` if it's annotated with `Flag`.

```py
# test.py

from mints import cli, Arg

@cli
def test(some: Arg):
    print(type(some))

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1
<class 'str'>
```

#### Default types

To parse a primitive type that is supported by the [`argparse`](https://docs.python.org/3/library/argparse.html#type), use the following syntax:
```py
# test.py

from mints import cli, Arg

@cli
def test(some: Arg[int]):
    print(type(some))

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1
<class 'int'>
```

#### User-defined types

To parse a custom type, register a parser function just for that.

You could use either the `parse` decorator:
```py
# test.py

from mints import cli, Arg

# User-defined type.
class Custom:
    def __init__(self, x):
        self.property = x

# A parser for user-defined type.
@cli.parse
def custom(x: str) -> Custom:
    return Custom(x)
      
@cli
def test(some: Arg[Custom]):
    print(some.property)

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1
1
```

Or the `add_parser` function:
```py
# test.py

from mints import cli, Arg

class Custom:        
    def __init__(self, x):
        self.property = x

@cli
def test(some: Arg[Custom]):
    print(some.property)

if __name__ == '__main__':
    cli.add_parser(Custom)
    cli()
```
```
$ python test.py 1
1
```

### Variable arguments

Variable arguments are also supported through the standard `List` type:
```py
# test.py

from typing import List

from mints import cli, Arg

@cli
def test(some: Arg[List[int]]):
    print(some)

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1 2 3
[1, 2, 3]
```

Note that lists are _non-greedy_:
```py
# test.py

from mints import cli, Arg

@cli
def test(x: Arg[int], y: Arg[List[int]], z: Arg[int]):
    print(x, y, z)

if __name__ == '__main__':
    cli()
```
```
$ python test.py 1 2 3 4
1 [2, 3] 4
```

Consider checking the [rolling dices](https://github.com/candy-kingdom/cli/blob/develop/examples/roll.py) example with a more realistic use case.

### Commands

Complex command line interfaces like `git` have several subcommands, e.g., `git status`, `git pull`, `git push`, etc.
These subcommands act as separate CLIs and, thus, should be defined as separate functions in Mints.

Consider the following example as a mock of `git` CLI:
```py
# git.py

from mints import cli, Flag

@cli
def git():
    ...

@git.command
def pull(rebase: Flag):
    if rebase:
        print('pulling with rebase')
    else:
        print('pulling')

@git.command
def push():
    print('pushing')

if __name__ == '__main__':
    cli()
```
```
$ python git.py pull
pulling
```
```
$ python git.py pull --rebase
pulling with rebase
```
```
$ python git.py push
pushing
```

Sometimes it's needed to have a deeper hierarchy of subcommands.
For example, the `dotnet` CLI tool allows calling [`dotnet tool install ...`](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install).

In Mints, this could be implemented in a natural way:
```py
# dotnet.py

from mints import cli

@cli
def dotnet():
    ...

@dotnet.command
def tool():
    ...

@tool.command
def install():
    ...

if __name__ == '__main__':
    cli()
```

## Learn more

Learn more by looking at our carefully prepared [examples](https://github.com/candy-kingdom/mints/blob/master/examples/).

## License

The package is licensed under the [MIT](https://github.com/candy-kingdom/mints/blob/master/LICENSE) license.

## Contributing

Before creating an issue or submitting a patch, check out our [contribution guildelines](https://github.com/candy-kingdom/mints/blob/master/CONTRIBUTING).
