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

In general, writing a CLI app is very similar to writing a "vanilla" function.
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
What types of arguments can be passed to the entry point depend on the signature of the function and the annotations being used to describe parameters.

In the following section we'll discuss how to implement positional arguments, flags and options for your CLI.

### Parameters

#### `Arg`

...

#### `Flag`

...

#### `Opt`

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
