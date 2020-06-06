# Contributing to {Name}

Thanks for considering to contribute.
We're open for any kind of contribution and help.
Feel free to send patches or opening issues.

## Creating an issue
Use one of our issue templates to either submit a bug or request a feature.

## Submitting a patch
To submit a _minor_ change (bugfix), just create a pull request with a clear and concise description of what you're trying to address.

To submit a _major_ change (feature, refactoring), link it with an open issue; consider creating one if needed.

Please, follow our conventions through the path.

## Conventions

We appreciate clean and elegant code, and we love to follow some conventions in our journey.

### Coding
- Use docstrings for each new class or function.
- Use [Google Style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstrings.
- Avoid creating utils or helper modules, classes or functions.
- Avoid using `get` in method names. For example, `get_item` should be `item`.


Consider checking the [source code](https://github.com/candy-kingdom/cli/blob/develop/candies/cli/cli.py) for a more detailed picture. 

### Commits
- Use clear and concise commit messages.
- Start a commit message with a verb in the past tense, then describe the meaning of change, end with a period. For example, `Added something.`, `Cleaned up something.`, `Removed something.`, ``Renamed `x` to `y`.``.

Note that we don't use the [imperative style](https://git.kernel.org/pub/scm/git/git.git/tree/Documentation/SubmittingPatches?id=HEAD#n133) for messages.

Consider checking the [commit history](https://github.com/candy-kingdom/cli/commits/develop) for a more detailed picture.
