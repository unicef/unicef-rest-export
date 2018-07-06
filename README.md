# UNICEF Rest Export

Django Rest Framework data export package


## Installation

    pip install unicef-rest-export


## Setup

Add ``unicef_rest_export`` to ``INSTALLED_APPS`` in settings

    INSTALLED_APPS = [
        ...
        'unicef_rest_export',
    ]


## Usage

TODO


## Contributing

### Environment Setup

To install the necessary libraries

    $ make install


### Coding Standards

See `PEP 8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ for complete details on the coding standards.

To run checks on the code to ensure code is in compliance

    $ make lint


### Testing

Testing is important and tests are located in `tests/` directory and can be run with;

    $ make test

Coverage report is viewable in `build/coverage` directory, and can be generated with;


### Project Links

 - Continuos Integration - https://circleci.com/gh/unicef/unicef-rest-export/tree/develop
 - Source Code - https://github.com/unicef/unicef-rest-export
