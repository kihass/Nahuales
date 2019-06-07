#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Auxiliary tools set"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
# External libraries
from os import chdir
from sys import platform


def configurePath4EspecialCase():
	"""Special configuration

	This configuration is to be able to use QPython3 and MGit, the problem is
	that when importing the local libraries QPython3 does not find the working
	folder, maybe it is a configuration problem, but I do not want to fix it :)
	"""
	if isAndroid():
		print('Changing working directory')

		chdir(
			'/storage/emulated/0/Android/data/com.manichord.mgit/files/' +
			'repo/NAHUALES/Nahuales/'
		)


def counter() -> int:
	number = 0

	while True:
		number += 1
		yield number


def isAndroid():
	"""Detects if the operating system is Android"""
	return (False, True)[platform.find('linux-armv') >= 0]


configurePath4EspecialCase()


if __name__ == '__main__':
	print('This library has no test code')
