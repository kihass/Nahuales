#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Circular file handling class"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
from hashlib import sha512 as defaultHash
from hashlib import sha256 as cryptHash
from os import path
import pyaes

from myBytesTools import bytes2int


class Circular_File_Synthesizer(object):
	"""Circular files synthesizer

	This class will take care of traversing the whole set of files indicated as a
	ring, for it will load the content of said files in the memory.
	"""

	__cntJmps = 0
	__data = b''
	__fileLists = []
	__flaCycleCrypt = False
	__lenData = None
	__pos = 0
	__seed = defaultHash()

	def __init__(self, argFilesList):
		"""Build the object and receive the list of circular files"""
		self.data = argFilesList[:]

	def __cycleCrypt(self) -> None:
		"""Flag to encrypt in each cycle"""
		if self.__flaCycleCrypt:
			if self.__cntJmps > self.__lenData:
				self.__cntJmps = 0
				self.crypt()

	def crypt(self) -> None:
		"""Encrypt data"""
		self.__seed.update(self.readInBytes(4))
		key = cryptHash(self.__seed.digest())

		aes = pyaes.AESModeOfOperationCTR(key.digest())
		#tmpData = self.__data.decode('utf-8')	# Error in crypt
		tmpData = self.__data.decode('latin1')
		self.__data = aes.encrypt(tmpData)

	def cycleCrypt(self, argStatus = True) -> None:
		"""Enable encrypt by cycle"""
		self.__flaCycleCrypt = argStatus

		if argStatus:
			self.__cntJmps = 0

	@property
	def data(self) -> bytes:
		"""Data

		Returns the contents of all files used in a circular form from the initial
		position
		"""
		return self.__data

	@data.setter
	def data(self, argFilesList: list) -> None:
		"""Receive the list of circular files that will be used"""
		if "%s" % type(argFilesList) in ["<class 'list'>", "<class 'tuple'>"]:
			self.__fileLists = argFilesList[:]
			self.__pos = 0

			# Tamaños de archivos
			for fn in argFilesList:
				with open(fn, mode='rb') as file:
					self.__data += file.read(path.getsize(fn))

			self.__lenData = len(self.__data)

		else:
			print('Fatal error: A list or tuple of files must be provided')
			print(type(argFilesList), "<", argFilesList, ">")

	@property
	def files(self) -> list:
		"""Returns the list of used files"""
		return self.__fileLists

	def jumpPos(self, argJump2Pos: int=1) -> None:
		"""Skip the positions indicated in the parameter

		If you skip a position, a negative number will indicate a setback
		"""
		if argJump2Pos < 0:
			self.__pos += argJump2Pos

			while self.__pos < 0:
				self.__pos += self.__lenData

		else:
			self.__pos = (self.__pos + argJump2Pos) % self.__lenData

	def readInBin(self, argSize: int=1) -> int:
		"""readInBin

		Read the indicated amount of data, if it is omitted it will only read one
		byte, a negative number indicates the reading of previous data
		"""
		self.__cycleCrypt()
		self.__cntJmps += argSize
		return bytes2int(self.readInBytes(argSize))

	def readInBytes(self, argSize: int=1) -> bytes:
		"""readInBytes

		Read the indicated amount of data, if it is omitted it will only read one
		byte, a negative number indicates the reading of previous data
		"""
		myBytesReturn = b''
		self.__cycleCrypt()

		if argSize < 0:
			self.jumpPos(argSize)
			argSize *= -1

		if self.__pos + argSize <= self.__lenData:
			myBytesReturn = self.__data[self.__pos: self.__pos + argSize]
			self.__pos += argSize

		else:
			myBytesReturn += self.__data[self.__pos:]
			self.__pos += argSize - self.__lenData

			while self.__pos >= self.__lenData:
				myBytesReturn += self.__data[:]
				self.__pos -= self.__lenData

			myBytesReturn += self.__data[0: self.__pos]

		self.__cntJmps += argSize
		return myBytesReturn

	@property
	def readInt(self) -> int:
		"""Read 4 bytes of the circular file and return an integer"""
		return bytes2int(self.readInBytes(4))

	@property
	def readIntHash(self) -> int:
		"""Same as readInt but first get the hash"""
		self.__seed.update(self.readInBytes(4))
		return bytes2int(self.__seed.digest()) % 2 ** 32

	@property
	def seed(self):
		return self.__seed.digest()

	@seed.setter
	def seed(self, argBytesSeed: bytes) -> None:
		"""Fix or update the seed with the bytes it receives"""
		self.__seed.update(argBytesSeed)


if __name__ == '__main__':
	"""Example of use"""
	from os import system

	system('cls')

	cfs = Circular_File_Synthesizer(['myCircularFileSynthesizer.py'])
	key = defaultHash(b'12345678')

	cfs.seed = key.digest()
	cfs.seed = cfs.data

	print('cfs.files:', cfs.files)
	print('cfs.readInBytes(10):', cfs.readInBytes(10))
	cfs.jumpPos(-10)
	print('cfs.jumpPos(-10)')
	print('cfs.readInBytes(10):', cfs.readInBytes(10))
	print('cfs.readInBytes(-10):', cfs.readInBytes(-10))
	print('cfs.readInt:', cfs.readInt)
	print('cfs.readIntHash', cfs.readIntHash)
	print('cfs.data[:50]:', cfs.data[:50])
	print('cfs.data[:50]:', cfs.data[:50].hex())
	cfs.crypt()
	print('cfs.crypt()')
	print('cfs.data[:50]:', cfs.data[:50])
	print('cfs.data[:50]:', cfs.data[:50].hex())
