#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Mohit Sharma",
    author_email='mohitsharma44@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Host based firewall using BPF and XDP",
    entry_points={
        'console_scripts': [
            'teleport_test_hbf=teleport_test_hbf.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='teleport_test_hbf',
    name='teleport_test_hbf',
    packages=find_packages(include=['teleport_test_hbf', 'teleport_test_hbf.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mohitsharma44/teleport_test_hbf',
    version='0.0.1',
    zip_safe=False,
)
