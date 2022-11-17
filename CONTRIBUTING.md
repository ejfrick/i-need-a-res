# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]
- [Roadmap]

[mit license]: https://opensource.org/licenses/MIT
[source code]: https://github.com/eng-jole/i-need-a-res
[documentation]: https://i-need-a-res.readthedocs.io/
[issue tracker]: https://github.com/eng-jole/i-need-a-res/issues
[roadmap]: https://github.com/ENG-Jole/i-need-a-res/milestones

## How to report a bug

Report bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker].

## How to set up your development environment

You need Python 3.10+ and the following tools:

- [Poetry]
- [Nox]
- [nox-poetry]

Install the package with development requirements:

```console
$ poetry install
```

You can now run an interactive Python session,
or the command-line interface:

```console
$ poetry run python
$ poetry run i-need-a-res
```

[poetry]: https://python-poetry.org/
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/

## How to test the project

Run the full test suite:

```console
$ nox
```

List the available Nox sessions:

```console
$ nox --list-sessions
```

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

```console
$ nox --session=tests
```

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/

## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this. Pre-beta, we are much more lax on checks; your PR will most likely be accepted if the targeted issue is successfuly resolved.
_We do not use merge commits_. Please only squash and merge PRs.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

```console
$ nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[pull request]: https://github.com/eng-jole/i-need-a-res/pulls

## Versioning & releases

### Versioning

We generally follow [semantic versioning]:

> Given a version number MAJOR.MINOR.PATCH, increment the:
>
> MAJOR version when you make incompatible API changes\
> MINOR version when you add functionality in a backwards compatible manner\
> PATCH version when you make backwards compatible bug fixes

We use [GitHub milestones] to indicate when we've reached a new release.
We tag commits on `main`, create a GitHub release, and keep a branch for each new release.
`main` should be treated as the latest possible "stable" version of the software.
It may not be feature complete, and the next commit to `main` may be a breaking change.

### Release process

1. Coordinate with contributors on who will cut the release.
2. Make your your local repo is up to date with `git fetch && git pull main`.
3. Run `git switch --create v<version> main`.
4. Run `poetry version <version>`. Do not include the `v` this time. Alternatively run `poetry version <bump_rule>` and provide a valid [bump rule].
5. If needed, update the [trove classifiers] in `pyproject.toml`
6. Run `git commit -m "I Need A Res v<version>" pyproject.toml`
7. Run `git push origin v<version>`
8. Open a pull request into `main` and get reviewed.
9. Squash and merge once all criteria are met. _Do not delete the branch_.
10. Contact a repo administrator to add the branch to the branch protection rules.

[semantic versioning]: https://semver.org
[github milestones]: https://github.com/ENG-Jole/i-need-a-res/milestones
[bump rule]: https://python-poetry.org/docs/cli/#version
[trove classifiers]: https://pypi.org/classifiers/

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md
