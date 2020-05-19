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
```shell
$ python3 say.py "Hi!" 
Hi!
```
```shell
$ python3 say.py "Hi!" --caps
HI!
```
```shell
$ python3 say.py "Hi!" --times 3
Hi!
Hi!
Hi!
```
```shell
$ python3 say.py --help
usage: say [-h] [--caps] [--times TIMES] phrase

Prints a phrase specified number of times.

positional arguments:
  phrase         A phrase to print.

optional arguments:
  -h, --help     show this help message and exit
  --caps         Whether to print phrase in upper-case.
  --times TIMES
```

## Install

```sh
$ pip install candy-cli
```

## Getting started

### Arguments

...

### Flags

...

### Options

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
