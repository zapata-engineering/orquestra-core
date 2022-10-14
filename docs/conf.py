# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from multiprocessing.sharedctypes import Value
import subprocess
import sys
import pathlib
import json
import os
from glob import glob
from pathlib import Path
import shutil
from distutils.dir_util import copy_tree
from tempfile import tempdir


repos_folder = os.path.abspath("repos")
TMP_MONOREPO_NAME = "tmp_monorepo"
currentfolder = Path(os.path.abspath("."))
temp_repo_folder = currentfolder / f"{TMP_MONOREPO_NAME}"

temp_repo_folder = str(temp_repo_folder)
sys.path.insert(0, temp_repo_folder)


def build_mono_repo(temp_repo_folder):

    subprocess.call(
        ["mkdir", "-p", temp_repo_folder], shell=True
    )  # make sure temporary folder exists

    # scan the manifest for the location of the root code directory for each repo
    with open(os.path.join(repos_folder, "manifest.json")) as fp:
        manifest = json.load(fp)

    for name, details in manifest["repos"].items():
        for path in details.get("autodoc", []):
            source_dir = str(Path(name) / path)
            print(f"source_dir: {source_dir} to tmp folder: {temp_repo_folder}")
            copy_tree(
                os.path.join(repos_folder, source_dir), temp_repo_folder
            )  # copy all folders to docs/tmp/repo/*


try:
    shutil.rmtree(temp_repo_folder)
except FileNotFoundError:
    print(f"no dir to remove {temp_repo_folder}")

build_mono_repo(temp_repo_folder)
# -- Project information -----------------------------------------------------

project = "Orquestra Core Docs"
copyright = "2022, Zapata Computing, Inc"

# The full version, including alpha/beta/rc tags
release = "0.2.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    # "sphinx.ext.doctest",
    "sphinx_design",
    # "sphinx.ext.graphviz",
    # "sphinxcontrib.youtube",
    # "sphinxcontrib.autoprogram",
    # "sphinxcontrib.confluencebuilder",
    "sphinx_copybutton",
    "sphinxemoji.sphinxemoji",
    "sphinx_togglebutton",
    "autoapi.extension",
]
source_suffix = {
    ".rst": "restructuredtext",
    # '.txt': 'restructuredtext',
    # '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "venv",
    "repos",
    "subtrees",
    "developer",
    "investigator",
    "src",
    "tests",
    "build",
    ".venv",
    ".github",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# this gets around some kind of bug-like behavior in autoapi where it doesn't create
# the entries for the index.rst unless there is an __init__.py despite
# setting autoapi_python_use_implicit_namespaces=True

autoapi_dirs = [os.path.join(temp_repo_folder, "orquestra")]
# autoapi_root = TMP_MONODOCS_NAME + "/api"
autoapi_root = "api"
for dirpath, dirnames, filenames in os.walk(temp_repo_folder):
    Path(dirpath, "__init__.py").touch()

html_logo = "_static/orquestra.png"
html_title = "Orquestra Core Documentation"
html_favicon = "_static/favicon.ico"

# Intersphinx is a tool for creating links to multiple repos.  This should help us!
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# This is so that the args to __init__ methods are appended to the class docs
autoclass_content = "both"

# set to true to see the contents of the autoapi directory after building
autoapi_keep_files = True
autoapi_python_use_implicit_namespaces = True

autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
    "undoc-members",
]
