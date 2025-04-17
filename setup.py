#!/usr/bin/env python3
# encoding=utf-8
# maintainer: rgaudin

import setuptools

setuptools.setup(
    name='ethiopian-date-converter',
    version='0.1.6',
    license='GNU General Public License (GPL), Version 3',

    provides=['ethiopian_date'],

    description='Ethiopian date converter.',
    long_description=open('README.rst').read(),

    url='https://github.com/dimagi/ethiopian-date-converter',

    packages=['ethiopian_date'],

    python_requires='>=3.8',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
