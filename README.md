# travelwhiz-dl

[![Python versions](https://img.shields.io/pypi/pyversions/travelwhiz_dl)](https://pypi.org/project/travelwhiz_dl/)
[![Release](https://img.shields.io/github/v/release/hulsiejames/travelwhiz-dl)](https://github.com/hulsiejames/travelwhiz-dl/releases)
[![Conda](https://img.shields.io/conda/v/conda-forge/travelwhiz_dl)](https://anaconda.org/conda-forge/travelwhiz_dl)
[![Tests](https://img.shields.io/github/actions/workflow/status/hulsiejames/travelwhiz-dl/tests.yml?label=tests)](https://github.com/hulsiejames/travelwhiz-dl/actions)
[![Coverage](https://img.shields.io/codecov/c/github/hulsiejames/travelwhiz-dl)](https://app.codecov.io/gh/hulsiejames/travelwhiz-dl)
[![Documentation](https://img.shields.io/readthedocs/travelwhiz-dl)](https://travelwhiz-dl.readthedocs.io/en/stable/)

automated python downloads of travelwhiz curated feeds

> This package is under development. Check the release notes before upgrading.

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

Describe the problem this package solves, who uses it and its main features here.
List planned features separately from features already available in a release.

## Installation

Once published to PyPI:

```sh
pip install travelwhiz_dl
```

If you also publish a conda-forge package:

```sh
conda install -c conda-forge travelwhiz_dl
```

Before publishing, install directly from GitHub:

```sh
pip install "git+https://github.com/hulsiejames/travelwhiz-dl"
```

Append `@v0.1.0` or a branch name to the Git URL to select a particular revision.
See [requirements.txt](requirements.txt) for runtime dependencies.

## Usage

```python
import travelwhiz_dl
```

Add a short working example here. If your package exposes a command line or GUI,
describe how to launch it and link to its guide.

## Documentation

The [documentation](https://travelwhiz-dl.readthedocs.io/en/stable/) includes
a quick-start guide, tutorials, examples and an API reference.

## Contributing

Open an [issue](https://github.com/hulsiejames/travelwhiz-dl/issues) to discuss bugs or ideas,
or submit a pull request. Install development dependencies with
`python -m pip install -e ".[dev,docs]"` and run `ruff check .`, `ruff format --check .`,
`pylint src`, `mypy src` and `pytest` before submitting changes.
See [LICENSE](LICENSE) for this package's licence.

## Contact

Maintained by James Hulse. Use the
[issue tracker](https://github.com/hulsiejames/travelwhiz-dl/issues) for package questions.

