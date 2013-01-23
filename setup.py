#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''Setuptools script.'''
import os

from setuptools import setup


os.environ['PYLINTRC'] = '.pylintrc'

VERSION = '0.1.0'
GITHUB_URL = 'https://github.com/bvox/keystoneclient-bvox-extension'


setup(name='keystoneclient-bvox-ext',
      version=VERSION,
      description="OpenStack Keystone client BVOX extension",
      long_description=open('README.rst', 'rt').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: Other/Proprietary License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='BVOX OpenStack Keystone client extension',
      author='Rafael Durán Castañeda',
      author_email='rafael@bvox.net',
      url=GITHUB_URL,
      download_url="%s/tarball/%s" % (GITHUB_URL, VERSION),
      license='Other/Proprietary License',
      py_modules=['keystoneclient_bvox_ext'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'python-keystoneclient>=0.2.2'
      ],
      tests_require=(
          'unittest2',
          'mox',
      ),
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      keystone-bvox = keystoneclient_bvox_ext:MAIN
      """,
      test_suite='tests',
      )
