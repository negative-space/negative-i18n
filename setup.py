#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://negative-i18n.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='negative-i18n',
    version='0.1.0',
    description='Database-stored translation strings for Django',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Alex Rudakov',
    author_email='ribozz@gmail.com',
    url='https://github.com/negative-space/negative-i18n',
    packages=[
        'negative_i18n',
    ],
    package_dir={'negative_i18n': 'negative_i18n'},
    include_package_data=True,
    install_requires=[
        'django-modeltranslation>=0.13b',
        'polib',
        'django>=2.0',
    ],
    license='MIT',
    zip_safe=False,
    keywords='negative-i18n',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)