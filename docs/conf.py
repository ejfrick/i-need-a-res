"""Sphinx configuration."""
project = "I Need A Res"
author = "Enny Jole"
copyright = "2022, Enny Jole"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
