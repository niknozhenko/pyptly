#!/usr/bin/env python
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pyptly import __version__


install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(req.req) for req in install_reqs]

setup(name="pyptly",
      version=__version__,
      description="Python wrapper for the Aptly API",
      license="MIT",
      author="Nikolai Nozhenko",
      author_email="nik.nozhenko@gmail.com",
      url="http://github.com/repelista/pyaptly",
      packages=find_packages(),
      install_requires=reqs,
      keywords="aptly library",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],
      zip_safe=True)
