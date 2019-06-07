#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""XOR in rotating cycles for bytes"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2019"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 19/02/2019"
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
from myBytesTools import int2bytes
from myBytesTools import ror4Bytes
from myBytesTools import xor4bytes
from myCircularFileSynthesizer import Circular_File_Synthesizer


def xcr4Bytes(
	argCFS: Circular_File_Synthesizer,
	argSeed: bytes,
	argRequiredBytes: int
) -> bytes:
	"""XOR in rotating cycles"""

	#### BEGIN Config ####
	maxSize = len(argCFS.data) - 8
	sizeInBytes = argCFS.readInt % maxSize + 8
	totalRounds = ceil(argRequiredBytes / sizeInBytes)
	#### END Config ####

	prevData = argCFS.readInBytes(sizeInBytes)

	for rounds in range(totalRounds):
		offset = argCFS.readInt % sizeInBytes

		sendData = argCFS.readInBytes(sizeInBytes)
		sendData = xor4bytes(ror4Bytes(sendData, offset), prevData)

		prevData = sendData

		if len(sendData) != sizeInBytes:
			print('Size error: len={} vs wanted:{} round:{}'.format(len(sendData), sizeInBytes, rounds))
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
	from testerTools import tests

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	iam = basename(__file__)[:-3]
	print('Example of use by {}'.format(iam))

	function = xcr4Bytes

	tests(function, False, False, False)
	tests(function, False, False, True)
	tests(function, True, False, False)
	tests(function, True, False, True)
	tests(function, False, True, False)
	tests(function, False, True, True)
