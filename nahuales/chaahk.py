#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Generador dinamico de numeros aleatorios """

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 20/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
from prngs.dpbprw import dpbprw
from myBytesTools import bytes2int
from myCircularFileSynthesizer import Circular_File_Synthesizer


class CHAAHK(object):
	"""(Mayan word for Rain) Dynamic random number generator"""
	# Catalog of methods to generate GNPA
	__catalog = None
	# Circular file
	__cfs = None
	# Generated flow
	__data = b''
	# Seed based on the hash of the key
	__seedKey = b''
	# Seed based on the hash of the files
	__seedFiles = b''
	# Flow size
	__sizeData = 0
	# Maximum size of the flow that will be generated
	__sizeMaxData = 0

	def __init__(
		self,
		argCfs: Circular_File_Synthesizer,
		argSeedKey: bytes,
		argSeedFiles: bytes,
		argRequiredSize: int
	):
		self.__cfs = argCfs
		self.__seedKey = argSeedKey
		self.__seedFiles = argSeedFiles
		self.__sizeMaxData = argRequiredSize
		self.__buildList()

	def __buildList(self):
		"""Build the catalog of methods for create GNPA"""
		self.__catalog = []

	def __selectorFromList(self, argList):
		"""Choise of GNBA"""
		return bytes2int(self.__cfs.readDataInBytes()) % len(argList)

	def __process(self):
		"""Calculate a random flow"""
		localData = b'0'

		if isinstance(self.__catalog, list):
			selFamN0 = bytes2int(self.__cfs.readDataInBytes()) % \
				len(self.__catalog)

			if isinstance(self.__catalog[selFamN0], list):
				# selFamN1 = bytes2int(self.__cf.readDataInBytes()) %\
				# 	len(self.__catalog[selFamN0])
				pass

			else:
				print("Esto no debería pasar")

		else:
			print("Esto no debería pasar")

		return localData

	def build(self):
		"""Build the selected flow until the desired size is obtained"""
		while self.__sizeData < self.__sizeMaxData:
			self.__data += self.__process()
			self.__sizeData = len(self.__data)

		return self.__data


if __name__ == '__main__':
	print('This library has no test code')
