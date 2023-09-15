<div align="center">
  <img height="120px" src="./logos/zeta.svg" />

  <h1 style="margin-top: 0px">Zeta Python SDK 🐍</h1>

  <p>
    <a href="https://badge.fury.io/py/zetamarkets-py"><img src="https://badge.fury.io/py/zetamarkets-py.svg" alt="PyPI version" height="18"></a>
    <a href="https://opensource.org/licenses/Apache-2.0"
      ><img
        alt="License"
        src="https://img.shields.io/badge/License-Apache%202.0-blueviolet"
    /></a>
    <a href="https://discord.gg/dD7YREfBkR"
      ><img
        alt="Discord Chat"
        src="https://img.shields.io/discord/841556000632078378?color=blueviolet"
    /></a>
  </p>
</div>

## Installation

### Install from Pypi

```sh
pip install zetamarkets_py
```

### Install from source

```sh
poetry install
```

## Usage

### Setting up a Solana wallet

Please follow the instructions here to setup a Solana wallet: https://docs.solana.com/wallet-guide/file-system-wallet.
By default the SDK will look for the wallet at `~/.config/solana/id.json`

### Running the examples

Run the various code examples provided in the [examples](./examples) directory.

## Development

### Formatting

We use [black](https://github.com/psf/black) with [isort](https://github.com/PyCQA/isort) for formatting.

```sh
poetry format
```

### Lint

We use [ruff](https://github.com/astral-sh/ruff) for linting.

```sh
poetry lint
```
