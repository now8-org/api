# Contributing

To contribute to this project, please follow these guidelines.

## Tests

Write tests for all your changes, including unit and integration tests if
appropriate.

## Commit message guidelines

Use the [Angular semantic versioning
format](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines):

```
{type_of_change}({scope}): {short_description}

{full_description}
```

Where:

* `type_of_change` is one of:

    * **build**: Changes that affect the build system or external dependencies.
    * **ci**: Changes to our CI configuration files and scripts.
    * **docs**: Documentation only changes.
    * **feat**: A new feature.
    * **fix**: A bug fix.
    * **perf**: A code change that improves performance.
    * **refactor**: A code change that neither fixes a bug nor adds a feature.
    * **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.).
    * **test**: Adding missing tests or correcting existing tests.

* `scope`: Name of the changed component.
* `short_description`: A succinct description of the change. It doesn't need to
    start with a capitalize letter nor end with a dot.
* `full_description`: A summary of the added changes.

### Commitizen

[Commitizen](https://commitizen-tools.github.io/commitizen/) is a tool that
defines a standard way of committing. It will help you write the commit
message and automatically bump the software version and generate a changelog.

Once install, start using `cz c` instead of `git commit`.

Other commands are:

  * `cz bump --changelog`: Automatic version bump.
  * `cz ch`: Update the changelog.

## Pull request guidelines

Aggregate your commits in a new branch with a meaningful name for the
changes and create a pull request from the web git interface so that other
team members can check your changes and propose modifications or approve it.

## Code quality checks

Use [psf/black](https://github.com/psf/black) (Python code formatter),
[PyCQA/flake8](https://github.com/PyCQA/flake8) (checks the style and
quality of some python code) and [python/mypy](https://github.com/python/mypy)
(Optional static typing for Python).

For even more quality checks, install the
[`pre-commit`](https://pre-commit.com/) configuration available in the root
directory of the repository with `pre-commit install`. This tool will
perform several checks before every commit.
