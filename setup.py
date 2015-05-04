# -*- coding: utf-8 -*-
"""
This module contains the tool of reduc.usermgr
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '5.0.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )


setup(name='reduc.ldap',
      version=version,
      description="Interface para acceso a LDAP",
      long_description=long_description,
      keywords='',
      author='RedUC',
      author_email='reduc@uc.edu.ve',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['reduc', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'python_ldap',
                        ],
      )
