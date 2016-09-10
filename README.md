[![Build Status](https://travis-ci.org/repelista/pyptly.svg?branch=master)](https://travis-ci.org/repelista/pyptly)
[![Coverage Status](https://coveralls.io/repos/github/repelista/pyptly/badge.svg?branch=master)](https://coveralls.io/github/repelista/pyptly?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pyptly.svg)](https://pypi.python.org/pypi/pyptly)

# pyptly
This library provides a Python interface to the Aptly API

### Dependencies:
- requests >= 2.4.3

### Installation:
From PyPI:

    pip install pyptly

Or you may use git to clone the repository from
Github and install it manually:

     python setup.py install

To build debian package run:

     dpkg-buildpackage -us -uc

### Basic Usage:

    api = pyptly.Aptly("http://127.0.0.1:8080")
    api.aptly_version()
    {u'Version': u'0.9.7'}
