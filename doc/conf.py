# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'therepy'
copyright = '2023, Hans Elliott'
author = 'Hans Elliott'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
master_doc = "index"

extensions = [
    "myst_nb",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme"
]
autoapi_dirs = ["../src/therepy"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = [".rst", ".md"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']


# -- Customize sphinx-autoapi ------------------------------------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/how_to.html#how-to-customise-what-gets-documented
def skip_submodules(app, what, name, obj, skip, options):
    if name.split(".")[-1].startswith("_"):
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_submodules)

