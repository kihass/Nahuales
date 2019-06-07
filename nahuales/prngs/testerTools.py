#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Tester tools set"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2019"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2019"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
# External libraries
from hashlib import sha512 as defaultHash
from os import makedirs
from os import remove
from os import stat
from os import system
from os.path import exists
from shutil import copy
from random import randint
from random import shuffle
from sys import path as syspath
from time import sleep
from time import time

syspath.append('..')

# Project libraries
from myCircularFileSynthesizer import Circular_File_Synthesizer
from myBytesTools import bin2Str
from myBytesTools import bytes2int

files = [
    ('data/originals/data.pi.bin', ),
    # https://gist.github.com/jsdario/6d6c69398cb0c73111e49f1218960f79
    ('data/originals/VeraCrypt.key', ),
    ('data/originals/sts-2_1_2.zip', ),
    ('data/originals/cryptopp565.zip', ),
    ('data/originals/Manglar.jpg', ),
    ('data/originals/Kuky.jpg', ),
    ('data/originals/nistspecialpublication800-22r1a.pdf', ),
    ('data/originals/librotmed.pdf', ),
    ('data/originals/Logo_Kike.png', ),
    ('data/originals/Glider.png', ),
    ('data/originals/gcc.1', ),
    ('data/originals/g77.1', ),
    ('data/originals/cpp.1', ),
    # C:\MinGW\man
    ('data/originals/el_quijote.txt', ),
    ('data/originals/randtest.py', ),
    ('data/originals/nahual.py', ),
    ('data/originals/dpbprw.py', ),
    ('data/originals/data.pi', ),
    ('data/originals/data.e', ),
]

fnRandomnessSummary = 'data/randomness_Summary.csv'

keysSize = 25

keys = [bytes([i % 256] if i // 256 == 0 else [i % 256, i // 256])
        for i in range(keysSize)]

minPValue = 0.01

# sizeOfTheStream=1048576
sizeOfTheStream = 1008000
sizeOfTheStream4Performance = 1000000


def end() -> None:
	if exists('data/stop'):
		exit()


def evalRandomnesOfFile(argFileName: str) -> float:
	if not exists("{}.report".format(argFileName)):
		argFileName = argFileName.replace('/','\\')
		cmd = 'py -2 ..\\randomtests_py2\\sp800_22_tests.py'
		cmd += ' "{}" > "{}.report"'.format(
			argFileName, argFileName)
		print('\n{}\n'.format(cmd))
		
		startTime = time()
		system(cmd)
		return time() - startTime

	else:
		return 0.0


def getDownloadAndTruncateFiles() -> list:
	"""Get the key files and place them in the directory for tests"""
	copy('../nahual.py', 'data/originals/nahual.py')
	copy('dpbprw.py', 'data/originals/dpbprw.py')
	copy('../testrandom/randtest.py', 'data/originals/randtest.py')

	# Create working directory, if not exists
	if not exists('data/analize'):
		makedirs('data/analize')

	vEvalListFiles = []
	files = []

	for shortFn in getKeyFilesNames():
		fileName = 'data/originals/{}'.format(shortFn)

		# Check size
		statInfo = stat("{}".format(fileName))

		# If too big
		if statInfo.st_size > getSizeOfTheStream():
			tmpName = "data/analize/{}.hatch".format(shortFn)
			files.append("{}.hatch".format(shortFn))

			if not exists(tmpName):
				print('Too big {}, hatch!'.format(fileName))
				tmpData = b''

				with open(fileName, mode='rb') as file:
					tmpData = file.read(getSizeOfTheStream())
					file.close()

				with open(tmpName, mode='wb') as file:
					file.write(tmpData)
					file.close()
			
			if not exists('{}.report'.format(tmpName)):
				vEvalListFiles.append(tmpName)
			
		else:
			tmpName = "data/analize/{}".format(shortFn)
			files.append("{}".format(shortFn))

			if not exists(tmpName):
				print('Copy {}'.format(fileName))
				copy(fileName, tmpName)

			if not exists('{}.report'.format(tmpName)):
				vEvalListFiles.append(tmpName)
	
	# They are processed separately for their impact on performance
	for fn in vEvalListFiles:
		fnReport = '{}.report'.format(fn)

		if not exists(fnReport) and exists('data/randomness'):
			spentTime = evalRandomnesOfFile(fn)
			randomnessSummary(fnReport, spentTime)

			print('\t{} s'.format(spentTime))

		# Verify if there is a termination file
		end()
		
	return files


def getKeyFilesNames() -> list:
	"""Returns the list of key files"""
	vFiles = []

	for fn in files:
		vFiles.append(fn[0].replace('data/originals/', ''))

	return vFiles


def getKeyFilesNamesFullPath() -> list:
	"""Returns the list of key files with full path"""
	vFiles = []
	
	for fn in files:
		vFiles.append(fn[0])

	return vFiles


def getKeys() -> list:
    """Returns the list of keys"""
    return keys


def getSizeOfTheStream() -> int:
    """Size of the data stream that will be generated for the tests"""
    return sizeOfTheStream


def getSizeOfTheStream4Performance() -> int:
    """Size of the data stream that will be generated for the performance calc"""
    return sizeOfTheStream4Performance


def myLockFile(argFileName: str, argId: int=0) -> None:
	"""Get the lock file

	argFileName	Name of the file to be blocked
	argId		Identifier for for this thread. If one is not provided, it will 			be randomly obtained
	"""
	lockFileName = "{}.lock".format(argFileName)
	waitTime = 3
	readData = float('+inf')
	
	if argId == 0:
		argId = randint(1, 2^64)

	while True:
		try:
			if exists(lockFileName):
				sleep(waitTime)
			else:
				# Add the identifier to the wait queue
				with open(lockFileName, mode='a') as file:
					file.write("%s\n" % argId)
					file.close()

				sleep(1)

				# Identify the one who arrived first
				with open(lockFileName, mode='r') as file:
					readData = int(file.readline())
					file.close()

				# Check if the verifier was the first to arrive and if so,
				# leave the blocking process
				if readData == argId:
					break
		except:
			pass


def myUnlockFile(argFileName: str, argId: int = 0) -> None:
	"""Release the lock file

	argFileName	Name of the file from which the lock file was generated
	argId		Identifier for for this thread. If one is not provided, it will 			be randomly obtained
	"""
	lockFileName = "{}.lock".format(argFileName)

	try:
		if exists(lockFileName):
			remove(lockFileName)
	except:
		pass


def randomnessSummary(argFileName: str, argSpentTime: float) -> None:
	"""Get the randomness summary"""
	if not exists(fnRandomnessSummary):
		output = 'testName, mode, cFn, idKey, bytes_generated, spentTime'
		output += ', approved, pvalue, monobit_test, pvalue, frequency_within_block_test, pvalue, runs_test, pvalue, '
		output += 'longest_run_ones_in_a_block_test, pvalue, binary_matrix_rank_test, pvalue, dft_test, pvalue, '
		output += 'non_overlapping_template_matching_test, pvalue, overlapping_template_'
		output += 'matching_test, pvalue, maurers_universal_test, pvalue, linear_complexity_test, pvalue, '
		output += 'serial_test, pvalue, approximate_entropy_test, pvalue, cumulative_sums_test, pvalue, '
		output += 'random_excursion_test, pvalue, random_excursion_variant_test\n'

		with open(fnRandomnessSummary, mode='w') as file:
			file.write(output)
			file.close()

	tmp = argFileName.split('/')
	testName = tmp[1] if tmp[1].find('_') == -1 else tmp[1][ : tmp[1].find('_')]
	mode = '' if tmp[1].find('_') == -1 else tmp[1][ tmp[1].find('_') + 1 :]
	cFn = tmp[2][:-7] if tmp[2].find('[') == -1 else tmp[2][: tmp[2].find('[')]
	cKey = '' if tmp[2].find('[') == -1 else tmp[2][ tmp[2].find('[') + 1 : -8]
	statInfo = stat("{}".format(argFileName[:-7]))
	sizeInBytes = statInfo.st_size
	spentTime = argSpentTime

	# print('\nargFileName:', argFileName)

	# print('TestName:', testName)
	# print('Mode:', mode)
	# print('cFn:', cFn)
	# print('cKey:', cKey)
	# print('sizeInBytes:', sizeInBytes)
	# print('spentTime:', spentTime)

	tmpOutput = ''
	output = '{}, {}, {}, {}, {}, {}, '.format(
		testName, mode, cFn, cKey, sizeInBytes, spentTime)
	cntPass = 0

	with open(argFileName) as file:
		flaWait = True

		while True:
			buffer = file.readline()

			if not buffer:
				break

			if flaWait:
				if '-------' in buffer:
					flaWait = False
			else:
				for i in range(6):
					buffer = buffer.replace('  ', ' ').replace('\t', ' ')

				buffer = buffer.strip()
				buffer = buffer.split(' ')

				isPASS = True if float(buffer[1]) >= minPValue else False
				cntPass += 1 if isPASS else 0

				tmpOutput += '{}, {}, '.format(buffer[1], 'PASS' if isPASS else 'FAIL')

	output += '{},{}\n'.format(cntPass, tmpOutput)

	# print(output)

	with open(fnRandomnessSummary, mode='a') as file:
		file.write(output)
		file.close()


def tests(argFunction,
		argIAm: str,
		argCrypt: bool = False,
		argRenewCryptByCycle: bool = False,
		argXOR: bool = False) -> None:
	"""Test function

	Build pseudorandom sequences and obtain metrics

	argFunction				Indicates the function of the test that will be
							executed
	argIAm					Name of script file
	argCrypt				Indicates that the cfs block will be encrypted
							once
	argRenewCryptByCycle	Indicates that cfs will renew encryption when 
							completing a reading cycle on cfs
	argXOR					Indicates that an XOR operation will be applied
							in each reading of cfs with the previous
							reading
	"""
	argId = ''

	if argXOR:
		argId += 'XOR'

	if argCrypt:
		argId += 'Crypt'

	if argRenewCryptByCycle:
		argId += 'RegenCrypt'
	
	print('\nTest for {}'.format(argId))

	# Get the key files and place them in the directory for tests
	files = getDownloadAndTruncateFiles()

	keys = getKeys()
	fnPerformance = 'data/performance_{}.csv'.format(argIAm)

	# Create working directory, if not exists
	if not exists('data/{}'.format(argId)):
		makedirs('data/{}'.format(argId))

	requiredInBytes = getSizeOfTheStream() // 8
	requiredInBytes4Performance = getSizeOfTheStream4Performance()

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
			# cfs.seed(cfs.data) and this updates the seed, but it
			# does not replace it
			cfs.seed = cfs.data

			# BEGIN Modes
			if argXOR:
				cfs.turnOnXORize()
				mode += 'XOR'

			if argCrypt:
				cfs.crypt()
				mode += 'Crypt'

			if argRenewCryptByCycle:
				cfs.crypt()
				cfs.renewCryptByCycle()
				mode += 'RegenCrypt'
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
				for data in argFunction(cfs, key,
											requiredInBytes4Performance):
					outputData += data

				spentTime = time() - startTime

				# Dump the data
				with open(fn, mode='wb') as file:
					file.write(outputData[:requiredInBytes])
					file.close()

				# BEGIN Record performance
				myLockFile(fnPerformance)

				if not exists(fnPerformance):
					with open(fnPerformance, mode='a') as file:
						file.write("testName, mode, cFn, idKey, bytes generated, spentTime\n")
						file.close()

				with open(fnPerformance, mode='a') as file:
					file.write("{}, {}, {}, {}, {}, {} \n".format(
						argId, mode, cFn, bytes2int(cKey),
						requiredInBytes4Performance, spentTime))
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

			if exists(fn) and exists('data/randomness'):
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


if __name__ == '__main__':
	"""Example of use"""
    # This block is to be able to use the sample code at the end of the file
    # External libraries
	from sys import path as syspath
	from os import system
	from os.path import basename
	import platform
	
	syspath.append('..')

	# Project libraries
	from myTools import counter
	from myBytesTools import bytes2int

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	print('Example of use by {}'.format(basename(__file__)[:-3]))

	print("\tFiles full path - getKeyFilesNamesFullPath()")
	cnt = counter()

	for fn in getKeyFilesNamesFullPath():
		print("{}. {}".format(next(cnt), fn))
	
	print("\n\tFiles - getKeyFilesNames()")
	cnt = counter()

	for fn in getKeyFilesNames():
		print("{}. {}".format(next(cnt), fn))

	print("\n\tKeys - getKeys()")
	cnt = counter()

	for fn in getKeys():
		print("{}. {}".format(next(cnt), bytes2int(fn)))

	print("\nSize of stream: {} - getSizeOfTheStream()".format(getSizeOfTheStream()))
	
	getDownloadAndTruncateFiles()

	remove('data/randomness_Summary.csv')
	randomnessSummary('data/analize/data.e.hatch.report', 100.0)
	randomnessSummary('data/test_mode/archivo[1234].report', 100.0)
