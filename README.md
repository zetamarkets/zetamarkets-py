<div align="center">
  <img height="120px" src="./logos/zeta-py.png" />

  <h1 style="margin-top: 0px">Zeta Python SDK 🐍</h1>

  <p>
    <a href="https://badge.fury.io/py/zetamarkets-py"><img src="https://badge.fury.io/py/zetamarkets-py.svg" alt="PyPI version" height="18"></a>
    <a href='https://zetamarkets-py.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/zetamarkets-py/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://opensource.org/licenses/Apache-2.0"
      ><img
        alt="License"
        src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"
    /></a>
    <a href="https://discord.gg/dD7YREfBkR"
      ><img
        alt="Discord Chat"
        src="https://img.shields.io/discord/841556000632078378?color=blueviolet"
    /></a>
  </p>
</div>

## Installation

### Install from PyPI

```sh
pip install zetamarkets_py
```

### Install from Source

You can add optional dependencies for running trading examples or docs using the `--with` flag.

```sh
poetry install [--with examples, docs]
```

## Usage

### Setting up a Solana wallet

Please follow the [Solana wallet creation docs](https://docs.solana.com/wallet-guide/file-system-wallet) to set up a wallet if you don't already have one locally.
By default the SDK will look for the wallet at `~/.config/solana/id.json`

### Running the examples

Run the various code examples provided in the [examples](https://zetamarkets-py.readthedocs.io/en/latest/examples.html#) directory.

## Development

### Formatting and Linting

We use [black](https://github.com/psf/black) with [isort](https://github.com/PyCQA/isort) for formatting and [ruff](https://github.com/astral-sh/ruff) for linting

```sh
poetry format
poetry lint
```
