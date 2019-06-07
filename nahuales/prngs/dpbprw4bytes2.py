#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""DPBPRW variant 2

Deterministic permutator based on pseudo random walkers (variant 2)"""

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
from math import ceil

if __name__ == '__main__':
	# This block is to be able to use the sample code at the end of the file
	from sys import path as syspath
	syspath.append('..')

# Project libraries
from myBytesTools import activeBits
from myBytesTools import bytes2int
from myBytesTools import getByte
from myBytesTools import int2bytes
from myBytesTools import replaceByte
from myBytesTools import xor4bytes
from myCircularFileSynthesizer import Circular_File_Synthesizer


def dpbprw4Bytes2(
	argCFS: Circular_File_Synthesizer,
	argSeed: bytes,
	argRequiredBytes: int
) -> bytes:
	"""Deterministic permutator based on pseudo random walkers (variant 2)"""
	if not isinstance(argRequiredBytes, int):
		argRequiredBytes = int(argRequiredBytes)

	# Config offset
	maxSize = len(argCFS.data) - 8
	sizeInBytes = (argCFS.readInt % maxSize) * 8 + 8
	sizeInBits = sizeInBytes // 8
	totalRounds = ceil(argRequiredBytes / sizeInBytes)
	
	prevData = argCFS.readInBytes(sizeInBytes)
	
	for rounds in range(totalRounds):
		newData = argCFS.readInBytes(sizeInBytes)
		vActives = activeBits(argCFS.readInBytes(sizeInBits))

		# Config offset
		offset1 = argCFS.readInt % sizeInBytes
		offset2 = 0

		# we make sure that the offset are different
		while True:
			offset2 = argCFS.readIntHash % sizeInBytes

			if offset1 != offset2:
				break

		# Permutations
		for pos in range(sizeInBytes):
			# Choose a new position
			if pos in vActives:
				newPos = (pos + offset1) % sizeInBytes

			else:
				newPos = (pos + offset2) % sizeInBytes
			
			voyager = getByte(prevData, pos)
			destiny = getByte(newData, newPos)
			voyager = xor4bytes(voyager, destiny)
			newData = replaceByte(newData, voyager, newPos)

		sendData = prevData = newData

		if len(sendData) != sizeInBytes:
			print('Size error: {} vs {} round:{}'.format(len(sendData), sizeInBytes, rounds))
			exit()

		# Send data
		if len(sendData) > argRequiredBytes:
			yield sendData[:argRequiredBytes]

		else:
			argRequiredBytes -= len(sendData)
			yield sendData


if __name__ == '__main__':
	"""Example of use"""
	# External libraries
	from os.path import exists
	from os import listdir
	from os import makedirs
	from os import stat
	from os import system
	from os.path import basename
	import platform
	from time import time

	# Project libraries
	from prngs.testerTools import tests

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	iam = basename(__file__)[:-3]
	print('Example of use by {}'.format(iam))

	function = dpbprw4Bytes2

	tests(function, False, False, False)
	tests(function, False, False, True)
	tests(function, True, False, False)
	tests(function, True, False, True)
	tests(function, False, True, False)
	tests(function, False, True, True)
