# -*- coding: utf8 -*-
"""Pyfalcon setup."""

from setuptools import setup

from pyfalcon import __version__

setup(
    name="pyfalcon",
    version=__version__,
    author="fatelei",
    author_email="fatelei@gmail.com",
    description="open falcon python client",
    install_requires=[
        "requests",
        "tornado"
    ],
    packages=["pyfalcon"],
    zip_safe=False,
    url="https://github.com/fatelei/pyfalcon",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
    ],
    license="BSD License"
)
