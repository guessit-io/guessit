#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

with io.open(os.path.join(here, 'HISTORY.rst'), encoding='utf-8') as f:
    history = f.read()

install_requires = ['rebulk', 'babelfish', 'python-dateutil']

setup_requires = ['pytest-runner']

dev_require = ['zest.releaser[recommended]', 'pylint', 'tox', 'sphinx', 'sphinx-autobuild']

tests_require = ['pytest>=3.3', 'pytest-benchmark', 'PyYAML']

package_data = ['config/*']

entry_points = {
    'console_scripts': [
        'guessit = guessit.__main__:main'
    ],
}

with io.open('guessit/__version__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]$', f.read(), re.MULTILINE).group(1)

args = dict(name='guessit',
            version=version,
            description='GuessIt - a library for guessing information from video filenames.',
            long_description=readme + '\n\n' + history,
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=['Development Status :: 5 - Production/Stable',
                         'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                         'Operating System :: OS Independent',
                         'Intended Audience :: Developers',
                         'Programming Language :: Python :: 2',
                         'Programming Language :: Python :: 2.7',
                         'Programming Language :: Python :: 3',
                         'Programming Language :: Python :: 3.4',
                         'Programming Language :: Python :: 3.5',
                         'Programming Language :: Python :: 3.6',
                         'Programming Language :: Python :: 3.7',
                         'Topic :: Multimedia',
                         'Topic :: Software Development :: Libraries :: Python Modules'
                         ],
            keywords='python library release parser name filename movies series episodes animes',
            author='Rémi Alvergnat',
            author_email='toilal.dev@gmail.com',
            url='http://guessit.readthedocs.org/',
            download_url='https://pypi.python.org/packages/source/g/guessit/guessit-%s.tar.gz' % version,
            license='LGPLv3',
            packages=find_packages(),
            package_data={'guessit': package_data},
            include_package_data=True,
            install_requires=install_requires,
            setup_requires=setup_requires,
            tests_require=tests_require,
            entry_points=entry_points,
            test_suite='guessit.test',
            zip_safe=True,
            extras_require={
                'test': tests_require,
                'dev': dev_require
            })

setup(**args)
