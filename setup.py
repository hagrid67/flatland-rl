#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# Gather requirements from requirements_dev.txt
# TODO : We could potentially split up the test/dev dependencies later
install_reqs = []
requirements_path = 'requirements_dev.txt'
with open(requirements_path, 'r') as f:
    install_reqs += [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]
requirements = install_reqs
setup_requirements = install_reqs
test_requirements = install_reqs

setup(
    author="S.P. Mohanty",
    author_email='mohanty@aicrowd.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Multi Agent Reinforcement Learning on Trains",
    entry_points={
        'console_scripts': [
            'flatland=flatland.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='flatland',
    name='flatland-rl',
    packages=find_packages('.'),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.aicrowd.com/flatland/flatland',
    version='0.1.1',
    zip_safe=False,
)
