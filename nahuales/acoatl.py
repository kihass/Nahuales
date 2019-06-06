#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase base para generadores de numeros aleatorios """

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 20/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$


class ACOATL(object):
	"""(Mayan word for Water Snake)

	Base class for deterministic pseudo-random flow generators
	"""
	__seed = b''      # Generator seed
	__expectancy = 0  # Life expectancy in cycles
	__age = 0         # Age in life cycles

	def reset(self, argSeed: bytes, argExpectancy: int):
		"""Start or restart the flow"""
		self.__age = 0
		self.__expectancy = argExpectancy
		self.__seed = argSeed

	def run(self, argCycles: int=0):
		"""Execute the indicated training cycles

		NOTE: This method must be redefined in the inheritance, since it is only a
		template
		"""
		cycles = 0
		data = b''

		if argCycles == 0:
			cycles = self.__expectancy - self.__age

		for c in range(cycles):
			print("Error: you are using the base class")
			# This must be replaced by the chosen generator function
			data += c

		return data


if __name__ == '__main__':
	print('This library has no test code')
