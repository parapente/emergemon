#! /usr/bin/env python
# -*- coding: utf-8

from distutils.core import setup

setup(name='emergeMon',
      version='0.1.0',
      description='Emerge Monitoring Application',
      author='Theofilos Intzoglou',
      author_email='int.teo@gmail.com',
      url='http://',
      classifiers=['License :: OSI Approved :: GNU General Public License (GPL)'],
      packages=['lib', 'ui'],
      package_dir={'': 'src'},
      package_data={'ui': ['emergemon.ui','emergemon.qrc','images/*']},
      scripts=['src/emergemon.py'],
      requires=['PyQt4'],
     )
