# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# import zetamarkets_py

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "zetamarkets_py"
copyright = "2023, Tristan0x"
author = "Tristan0x"
# The short X.Y version.
# version = zetamarkets_py.__version__
# The full version, including alpha/beta/rc tags.
# release = version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    # 'sphinx.ext.autosummary',
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

# Use Google style docstrings
napoleon_google_docstring = True
# napoleon_use_param = False
# napoleon_use_ivar = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

autosummary_generate = True
