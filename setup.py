#!/usr/bin/env python
from setuptools import setup, find_packages
from pyptly import __version__

setup(name="pyptly",
      version=__version__,
      description="Python wrapper for the Aptly API",
      license="MIT",
      author="Nikolai Nozhenko",
      author_email="nik.nozhenko@gmail.com",
      url="http://github.com/repelista/pyaptly",
      packages=find_packages(exclude=['tests']),
      install_requires=reqs,
      keywords="aptly library",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
      ],
      zip_safe=True)
