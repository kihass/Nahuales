#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Doctorate Project"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
from getpass import getpass
from hashlib import sha512 as defaultHash
from os import path
import os

from chaahk import CHAAHK
from myBytesTools import bytes2int
from myBytesTools import xor4bytes
from myCircularFileSynthesizer import Circular_File_Synthesizer
from myTools import isAndroid


class NAHUAL(object):
	# Key files that will be used in a circular manner
	__cFsk = None
	# Output file name
	__fnOutputFile = ""
	# (Bytes) Binary representation of key files hash
	__hashFilesKey = b''
	# (Bytes) Binary representation of the key hash
	__hashKey = b''
	# (Bytes) Binary version of the message
	__inputData = b''
	# (Bytes) Processed data output
	__outputData = b''
	# (Bytes) Output file
	__outputFile = b''

	def loadMsg(self, argFileName: str):
		"""Load the message file that will be processed"""
		msgLen = os.path.getsize(argFileName)

		with open(argFileName, mode='rb') as file:
			self.__inputData = file.read(msgLen)
			file.close()

	def captureKey(self):
		"""Capture the key encryption with keyboard"""
		key1 = getpass('Teclee el password:  ')
		key2 = getpass('Teclealo nuevamente: ')

		if key1 == key2:
			self.key = key1

	def run(self):
		"""Execute the encryption or decryption operation"""
		gf = CHAAHK(
			self.__cFsk,
			self.__hashKey,
			self.__hashFilesKey,
			len(self.__inputData)
		)

		self.__outputData = xor4bytes(
			self.__inputData, gf.build()
		)

		with open(self.__fnOutputFile, mode='wb') as file:
			file.write(self.__outputData)
			file.close()

	def mask(self, argSize):
		gf = CHAAHK(
			self.__cFsk,
			self.__hashKey,
			self.__hashFilesKey,
			argSize
		)

		self.__outputData = gf.build()

		with open(self.__fnOutputFile, mode='wb') as file:
			file.write(self.__outputData)
			file.close()

	@property
	def key(self):
		"""Returns the current status of key"""
		return self.__hashKey

	@key.setter
	def key(self, argKey: str):
		"""Receive the key, make the hash and store as a integer"""
		if isinstance(argKey, str):
			self.__hashKey = defaultHash(str.encode())

		else:
			print("Fatal error the key must be a text string")

	@property
	def keyFiles(self):
		"""Returns key files list"""
		return self.__cFsk.files

	@keyFiles.setter
	def keyFiles(self, argFilesLists: list):
		"""List of files that are used as a key"""
		self.__cFsk = Circular_File_Synthesizer(argFilesLists)
		self.__hashFilesKey = defaultHash(self.__cFsk.data)

	@property
	def msg2Bin(self):
		"""Returns the message in binary representation"""
		return bytes2int(self.__inputData)

	@property
	def msg2Bytes(self):
		"""Return the message in "bytes" representation"""
		return self.__inputData

	@property
	def msg2Hex(self):
		"""Returns the message in binary representation"""
		if isAndroid():
			return hex(bytes2int(self.__inputData)).replace(
				'0x', '')
		else:
			return self.__inputData.hex()

	@property
	def msg2Str(self):
		"""Return the message in plain text"""
		return self.__inputData.decode()

	@msg2Str.setter
	def msg2Str(self, argMsg: str):
		"""Encode the message in binary"""
		self.__inputData = str.encode(argMsg)

	@property
	def outputFile(self):
		"""Returns output file name"""
		return self.__fnOutputFile

	@outputFile.setter
	def outputFile(self, argFileName: str):
		"""Set name of output file"""
		self.__fnOutputFile = argFileName


if __name__ == '__main__':
	print('This library has no test code')
