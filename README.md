# {Name}

[![Build](https://github.com/candy-kingdom/cli/workflows/Build/badge.svg)](https://github.com/JoshuaLight/chalice-restful/actions)

_Clean and elegant CLI development kit._

## Overview

{Name} is a micro-framework that allows you to build CLI apps in declarative and natural way.
It's a lightweight alternative to Click, Plac or Fire with the annotations based API.

Consider a following example as a demonstration of {Name} capabilities:
```py
# say.py

from candies.cli import cli, Arg, Flag, Opt

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

It then can be used like that:
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
$ pip install candy-cli
```

## Getting started

In general, writing a CLI app is very similar to writing a regular function.
{Name} is based on this metaphor, allowing to describe the whole interface of the app using only a function signature.
Consider the following example:
```py
# print.py

from candies.cli import cli, Arg

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
Annotate a parameter of a function with it to make it positional.

Positional arguments work in same way as in programming languages.
Consider this function:
```py
# test.py

@cli
def entry(x: Arg, y: Arg):
    ...
```

It allows the following call in shell:
```
$ python test.py 1 2
```

But not:
```
$ python test.py 1
```

Or:
```
$ python test.py 1 2 3
```

It's possible though to add a default value for an argument:
```py
# test.py

@cli
def entry(x: Arg, y: Arg = 2):
    ...
```

To support the following:
```
$ python test.py 1
```

Note: it's not possible to define something like this:
```py
# test.py

@cli
def entry(x: Arg = 1, y: Arg):
    ...
```

The function signature is not supported even in Python.

#### `Flag`

...

#### `Opt`

...

#### Types

...

### Commands

...

### Help

...

## Learn more

...

## License

The package is licensed under the [MIT](https://github.com/candy-kingdom/cli/blob/master/LICENSE) license.

## Contributing

...
