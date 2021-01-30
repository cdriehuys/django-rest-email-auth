#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# django-rest-email-auth documentation build configuration file, created
# by sphinx-quickstart on Fri Nov  3 12:44:08 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.

import os


# -- General configuration ---------------------------------------------


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinxcontrib.httpdomain", "sphinx_issues"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "django-rest-email-auth"
copyright = "2017, Chathan Driehuys"
author = "Chathan Driehuys"

# The version info for the project you're documenting, acts as
# replacement for |version| and |release|, also used in various other
# places throughout the built documents.
#
# The short X.Y version.
version = "3.0.2"
# The full version, including alpha/beta/rc tags.
release = "3.0.2"

# The language for content autogenerated by Sphinx. Refer to
# documentation for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce
# nothing.
todo_include_todos = False


# Configuration for 'sphinx-issues'
issues_github_path = "cdriehuys/django-rest-email-auth"


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.
if os.environ.get("READTHEDOCS") == "True":
    html_theme = "default"
else:
    html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ["_static"]


# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "django-rest-email-authdoc"


# -- Options for LaTeX output ------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "django-rest-email-auth.tex",
        "django-rest-email-auth Documentation",
        "Chathan Driehuys",
        "manual",
    )
]


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "django-rest-email-auth",
        "django-rest-email-auth Documentation",
        [author],
        1,
    )
]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "django-rest-email-auth",
        "django-rest-email-auth Documentation",
        author,
        "django-rest-email-auth",
        "One line description of project.",
        "Miscellaneous",
    )
]
