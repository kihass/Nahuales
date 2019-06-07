#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""DPBPRW

Deterministic permutator based on pseudo random walkers """

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
from myBytesTools import int2bytes
from myCircularFileSynthesizer import Circular_File_Synthesizer


def dpbprw(
	argCFS: Circular_File_Synthesizer,
	argSeed: bytes,
	argRequiredBytes: int
) -> bytes:
	""" Deterministic permutator based on pseudo random walkers """

	#### BEGIN Config ####
	maxSize = argSeed.digest_size
	sizeInBytes = argCFS.readInt % maxSize + 1
	sizeInBytes = 2 if sizeInBytes < 2 else sizeInBytes
	sizeInBits = sizeInBytes * 8
	totalRounds = ceil(argRequiredBytes / sizeInBytes)

	# Config offset
	offset1 = argCFS.readInt % sizeInBits
	offset2 = 0

	# We make sure that the offset are different
	while True:
		offset2 = argCFS.readIntHash % sizeInBits

		if offset1 != offset2:
			break
	
	prevData = argCFS.readInBin(sizeInBytes)
	#### END Config ####

	for rounds in range(totalRounds):
		#### BEGIN ConfigLocal ####
		newData = argCFS.readInBin(sizeInBytes)
		vActives = activeBits(argCFS.readInBytes(sizeInBytes))
		#### END ConfigLocal ####

		# Permutations
		for pos in range(sizeInBits):
			# Choose a new position
			if pos in vActives:
				newPos = (pos + offset1) % sizeInBits

			else:
				newPos = (pos + offset2) % sizeInBits

			voyager = (prevData >> pos & 0b1) << newPos
			newData ^= voyager

		prevData = newData

		sendData = int2bytes(newData, sizeInBytes)

		if len(sendData) != sizeInBytes:
			print('Size error: {} vs {} round:{}'.format(len(sendData), sizeInBytes, rounds))

		# Send data
		if len(sendData) > argRequiredBytes:
			yield sendData[:argRequiredBytes]

		else:
			argRequiredBytes -= len(sendData)
			yield sendData


if __name__ == '__main__':
	"""Example of use"""
	from hashlib import sha512 as defaultHash
	from os.path import exists
	from os import listdir
	from os import makedirs
	from os import stat
	from os import system
	import platform
	from random import shuffle
	from time import time

	from myBytesTools import bin2Str
	from myBytesTools import bytes2int
	from testerTools import evalRandomnesOfFile
	from testerTools import fnRandomnessSummary
	from testerTools import getDownloadAndTruncateFiles
	from testerTools import getKeys
	from testerTools import getSizeOfTheStream
	from testerTools import myLockFile
	from testerTools import myUnlockFile
	from testerTools import end
	

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	# Get the key files and place them in the directory for tests
	files = getDownloadAndTruncateFiles()

	keys = getKeys()
	fnPerformance = 'data/performance.csv'

	def tests(argId: str,
			argFunction,
			argCrypt: bool = False,
			argRenewCryptByCycle: bool = False,
			argXOR: bool = False) -> None:
		"""Test function

		Build pseudorandom sequences and obtain metrics

		argId 					Indicates the identifier of the test that will
								be run
		argFunction				Indicates the function of the test that will be
								executed
		argCrypt				Indicates that the cfs block will be encrypted
								once
		argRenewCryptByCycle	Indicates that cfs will renew encryption when 
								completing a reading cycle on cfs
		argXOR					Indicates that an XOR operation will be applied
								in each reading of cfs with the previous
								reading
		"""
		print('\nTest for {}'.format(argId))

		# Create working directory, if not exists
		if not exists('data/{}'.format(argId)):
			makedirs('data/{}'.format(argId))

		requiredInBytes = getSizeOfTheStream() // 8
		mode = ''

		# Keys and files are mixed to facilitate their processing in parallel,
		# thus blocking by mutual exclusion is difficult to follow the same
		# sequence of tasks
		shuffle(files)
		shuffle(keys)

		# Build pseudorandom sequences
		for cFn in files:
			for cKey in keys:
				cfs = Circular_File_Synthesizer(('data/analize/{}'.format(cFn),))
				hashFilesKey = defaultHash(cfs.data)
				key = defaultHash(cKey)
				key.update(hashFilesKey.digest())

				# Inital config of circular file
				cfs.seed = key.digest()
				# Because seed is a setter, cfs.seed = cfs.data equals to
				# cfs.seed (argBytesSeed) and this updates the seed, but it 
				# does not replace it
				cfs.seed = cfs.data

				# BEGIN Modes
				if argCrypt:
					cfs.crypt()
					mode += 'Crypt'

				if argRenewCryptByCycle:
					cfs.crypt()
					cfs.renewCryptByCycle()
					mode += 'RegenCrypt'

				if argXOR:
					cfs.turnXORize()
					mode += 'XOR'
				# END Modes

				cfs.jumpPos(cfs.readIntHash % len(cfs.data))

				# Build output file name
				fn = "data/{}/{}-[{}].mask".format(argId, cFn, bytes2int(cKey))

				if not exists(fn):
					# When you create it, prevent another thread from taking it
					with open(fn, mode='wb') as file:
						file.close()

					print("Build: {}".format(fn))
					outputData = b''

					startTime = time()

					# Note: argFunction is a generator or iterator
					# in other words, is a equivalent at lazy function
					for data in argFunction(cfs, key, requiredInBytes):
						outputData += data

					spentTime = time() - startTime

					# Dump the data
					with open(fn, mode='wb') as file:
						file.write(outputData)
						file.close()

					# BEGIN Record performance
					myLockFile(fnPerformance)

					if not exists(fnPerformance):
						with open(fnPerformance, mode='a') as file:
							file.write("testName, mode, cFn, idKey, bytes generated, spentTime\n")
							file.close()

					with open(fnPerformance, mode='a') as file:
						file.write("{}, {}, {}, {}, {}, {} \n".format(
							argId, mode, cFn, bytes2int(cKey), requiredInBytes, 
							spentTime))
						file.close()

					myUnlockFile(fnPerformance)
					# END Record performance

					print('\t{} s'.format(spentTime))

					# Verify if there is a termination file
					end()

		# Keys and files are mixed to facilitate their processing in parallel,
		# thus blocking by mutual exclusion is difficult to follow the same
		# sequence of tasks
		shuffle(files)
		shuffle(keys)

		# Evaluate randomness
		# This section is separated since it consumes most of the processing
		for cFn in files:
			for cKey in keys:
				fn = "data/{}/{}[{}].mask".format(argId, cFn, bytes2int(cKey))

				if exists(fn):
					spentTime = evalRandomnesOfFile(fn)

					output = ''

					myLockFile(fnPerformance)

					with open(fnRandomnessSummary, mode='w') as file:
						file.write(output)
						file.close()

					myUnlockFile(fnPerformance)

					# Verify if there is a termination file
					end()
		
		print('Complete {}'.format(argId))

	tests('dpbprw_raw',		  dpbprw, False, False, False)
	tests('dpbprw_XORraw',	  dpbprw, False, False, True)
	tests('dpbprw_crypt',	  dpbprw, True,  False, False)
	tests('dpbprw_XORcrypt',  dpbprw, True,  False, True)
	tests('dpbprwr_regen',	  dpbprw, False, True,  False)
	tests('dpbprwr_XORregen', dpbprw, False, True,  True)
