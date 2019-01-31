############
Contributing
############

We welcome contributions to this project. For non-trivial improvements, we would encourage discussion in a GitHub issue before opening a pull request. This is also a great contribution in and of itself as it lets us know where to focus development efforts.


*************
Project Setup
*************

The first step is to fork the repository and clone it to your computer. Once you have done that, we recommend setting up a virtual environment to encapsulate the project's dependencies. To install the third-party packages required by the project, run::

    pip install -e .

Based on the contribution you are making, you may have to install additional dependencies.

.. code-block:: bash

    # To run tests
    pip install -r requirements/test.txt

    # To build documentation locally
    pip install -r requirements/docs.txt

Linting
=======

We use black_ for code formatting and flake8_ for linting. Code that fails the checks performed by either of these tools will cause the build to fail. To easily perform these checks on every commit, we recommend using the excellent ``pre-commit`` tool.

.. code-block:: bash

    pip install pre-commit
    pre-commit install


*******
Testing
*******

This project contains a comprehensive test suite. To run the tests locally, make sure the test requirements are installed and then execute::

    pytest


**********************
Opening a Pull Request
**********************

Once you have made your contribution and pushed it to your fork of the repository, please `open a pull request <pull-request_>`_. The pull request description should contain a concise description of the change made and link to the issue that it addresses.


.. _black: https://github.com/ambv/black
.. _flake8: http://flake8.pycqa.org/en/latest/
.. _pull-request: https://github.com/cdriehuys/django-rest-email-auth/compare
