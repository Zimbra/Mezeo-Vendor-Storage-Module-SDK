#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='company_vendormodules',
    version='1.0',
    description='Vendor Storage Modules for company',
    long_description='Vendor Storage Modules for company',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    author='company',
    author_email='support@example.com',
    url='http://www.example.com',
    packages=find_packages(exclude=['modules', 'simple', 'tests', 'tests.*']),
    license='License :: Other/Proprietary License',
    test_suite="nose.collector",
)
