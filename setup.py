#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-sentry-400-middleware',
    version='0.3.0',
    description='Django middleware to log 400 level errors to Sentry.',
    author='Art Processors',
    author_email='operations@artprocessors.net',
    url='https://github.com/ArtProcessors/django-sentry-400-middleware',
    packages=find_packages(),
    install_requires=['django', 'raven'],
    extras_require={
        'dev': [
            'mock',
            'pytest',
        ]
    }
)
