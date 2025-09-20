############
Contributing
############

We welcome contributions to this project. For non-trivial improvements, we would
encourage discussion in a GitHub issue before opening a pull request. This is
also a great contribution in and of itself as it lets us know where to focus
development efforts.


*************
Project Setup
*************

The first step is to fork the repository and clone it to your computer. Once you
have done that, the easiest way to ensure you have the correct dependencies is
to use the devcontainer packaged in the repository. If you aren't using the
devcontainer, you may have to install some tools on your own. To install the
development dependencies, run::

    poetry install

Based on the contribution you are making, you may have to install additional
dependencies.

.. code-block:: bash

    # For documentation builds
    poetry install --with docs,docs-dev

Linting
=======

We use black_ for code formatting and flake8_ for linting. Code that fails the
checks performed by either of these tools will cause the build to fail. To
easily perform these checks on every commit, we recommend using the excellent
``pre-commit`` tool.

As a one-time setup step, install the pre-commit hook in your local repository:

.. code-block:: bash

    poetry run pre-commit install


*******
Testing
*******

This project contains a comprehensive test suite. To run the tests locally, make
sure the test requirements are installed and then execute::

    poetry run pytest


**********************
Opening a Pull Request
**********************

Once you have made your contribution and pushed it to your fork of the
repository, please `open a pull request <pull-request_>`_. The pull request
description should contain a concise description of the change made and link to
the issue that it addresses.


.. _black: https://github.com/ambv/black
.. _flake8: http://flake8.pycqa.org/en/latest/
.. _pull-request: https://github.com/cdriehuys/django-rest-email-auth/compare
