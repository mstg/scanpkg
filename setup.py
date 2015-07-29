#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Mustafa
# @Date:   2015-07-10 00:06:09
# @Last Modified by:   Mustafa
# @Last Modified time: 2015-07-30 00:50:20

import os
from setuptools import setup

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('scanpkg/__version__.py', 'r') as f:
    exec(f.read())

setup(
	name = "scanpkg",
	version = __version__,
	author = "mstg",
	author_email = "mustiigezen@gmail.com",
	description = ("Windows alternative for dpkg-scanpackages (mainly created for cydia repos, but should work with other Debian repos)"),
	license = read("LICENSE"),
	keywords = "dpkg scanpackages scanpkg windows dpkg-scanpackages",
	url = "https://github.com/mstg/scanpkg",
	download_url = "https://github.com/mstg/scanpkg/tarball/" + __version__,
	packages=['scanpkg'],
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	entry_points = {
		'console_scripts': [
			'scanpkg = scanpkg.scanpkg:main',
		],
	},
	install_requires=['patool', 'click'],
	include_package_data = True,
)