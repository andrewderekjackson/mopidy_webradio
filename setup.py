#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'setuptools',
    'Mopidy >= 0.14',
    'Pykka >= 1.1'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='mopidy_test',
    version='0.1.0',
    description="My first test plugin.",
    long_description=readme + '\n\n' + history,
    author="Andrew Jackson",
    author_email='andrewderekjackson@gmail.com',
    url='https://github.com/andrewderekjackson/mopidy_test',
    packages=[
        'mopidy_test',
    ],
    entry_points={
        'mopidy.ext': [
            'test = mopidy_test:Extension',
        ],
    },
    package_dir={'mopidy_test':
                 'mopidy_test'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='mopidy_test',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
