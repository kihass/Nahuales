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
# External librarie
from hashlib import sha512 as defaultHash
from os import chdir
from os import makedirs
from os import remove
from os import stat
from os import system
from os.path import basename
from os.path import dirname
from os.path import exists
import pyaes
from shutil import copy
from shutil import copytree
from random import randint
from random import shuffle
from os.path import splitext
from sys import path as syspath
from time import sleep
from time import time
from urllib.request import urlretrieve

syspath.append('..')

# Project libraries
from acmdr import acmdr
from dpbprw import dpbprw
from dpbprw2 import dpbprw2
from dpbprw4bytes import dpbprw4Bytes
from dpbprw4bytes2 import dpbprw4Bytes2
from myBytesTools import bytes2int
from myBytesTools import bin2Str
from myCircularFileSynthesizer import Circular_File_Synthesizer
from tstMyListOfTestFiles import FilesNames
from tstMyListOfTestFiles import keys
from tstMyListOfTestFiles import minPValue
from tstMyListOfTestFiles import sizeOfTheStream
from tstMyListOfTestFiles import sizeOfTheStream4Performance
from xcr import xcr
from xcr4bytes import xcr4Bytes


directoryOfOrigins = 'data/originals/'
analysisDirectory = 'data/analize/'
fnRandomnessSummary = 'data/randomness_Summary.csv'
testList = [acmdr] 


def downloadFile(argURL: str, argDestination: str) -> None:
	urlretrieve(argURL, argDestination)


def stopRequest() -> None:
	if exists('data/stop'):
		exit()


def evalRandomnesOfFile(
	argFileName: str, 
	argSizeFile: int, 
	argReportsDir: str,
	argSpendTime2MakeStream: int = 0,
	argProof: str='',
	argKey: str='',
	argBaseDir: str='',
	):
	"""Run the randomness evaluation tool, then generate the summary and return
	the time spent

	argFileName		Nombre del archivo
	argSizeFile		Tamaño del archivo
	argReportsDir	Carpeta	 donde se encuentra el reporte y a donde se copio la STS
	argSpendTime2MakeStream
	argProof
	argKey
	argBaseDir
	"""
	if not exists("{}.report".format(argFileName)):
		statInfo = stat("{}".format(argFileName[:-7]))
		sizeInBits = statInfo.st_size * 8
		fn, ext = splitext(basename(argFileName))
		ext = ext[1:]

		# TODO Agregar directorio de trabajo
		pathSTS = 'STS_v5.0.2/Binaries_for_Windows/x64_with_FFTW/'
		cmd = '{}{}'.format(argReportsDir, pathSTS)
		cmd += 'NIST.exe -fast -file {} '.format(argFileName)
		cmd += '-streams 1 -tests 111111111111111 -defaultpar -fileoutput '
		cmd += '-binary {}'.format(sizeInBits)
		cmd = cmd.replace('/', '\\')
		print('\n{}\n'.format(cmd))

		startTime = time()
		system(cmd)
		# copy to reportsDir
		spendTime2Eval = time() - startTime
		
		# TODO Revisar parametros argSpendTime2MakeStream
		score, output = readReports(pathSTS, argProof, ext, fn,
				argSizeFile, argKey, spendTime2Eval)
		randomnessSummary(output)

		return score

	else:
		return 0.0










def copySTS(argPath: str):
	"""
	Copy the test directory to the reports folder. Because the reports are 
	created in the same folder, it is not possible to analyze multiple files 
	at the same time, for that reason a copy is created, in this way it is 
	possible to execute several tests, only in different directories.
	"""
	pathSTS = '../STS_v5.0.2/Binaries_for_Windows/x64_with_FFTW/'
	targetPath = '{}/sts/'.format(argPath)

	if not exists(targetPath):
		makedirs(destinationPath)
	
	copy('{}libfftw3-3.dll'.format(pathSTS),
			'{}libfftw3-3.dll'.format(targetPath))
	copy('{}NIST.exe'.format(pathSTS),
			'{}NIST.exe'.format(targetPath))
	copytree(pathSTS, '{}/sts/'.format(argPath))


def getDownloadAndTruncateFiles():
	"""Get the key files and place them in the directory for tests"""
	copy('../nahual.py', '{}nahual.py'.format(directoryOfOrigins))
	copy('dpbprw.py', '{}dpbprw.py'.format(directoryOfOrigins))
	copy('../testrandom/randtest.py', '{}randtest.py'.format(directoryOfOrigins))

	# Create working directory, if not exists
	if not exists(analysisDirectory):
		makedirs(analysisDirectory)

	files = FilesNames()

	# They are processed separately for their impact on performance
	for fn in files.scrollFileNames():
		fnReport = files.report()

		if not exists(fnReport) and exists('data/randomness'):
			# TODO Corregir parametros que se agregaron
			spentTime = evalRandomnesOfFile(fn)
			randomnessSummary(fnReport, spentTime)

			print('\t{} s'.format(spentTime))

		# Verify if there is a stop request
		stopRequest()


def getKeys() -> list:
    """Returns the list of keys"""
    return keys


def myLockFile(argFileName: str, argId: int = 0) -> None:
	"""Get the lock file

	argFileName	Name of the file to be blocked
	argId		Identifier for for this thread. If one is not provided, it will 			be randomly obtained
	"""
	lockFileName = "{}.lock".format(argFileName)
	waitTime = 3
	readData = float('+inf')

	if argId == 0:
		argId = randint(1, 2 ^ 64)

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


def randomnessSummary(argOutput: str) -> None:
	"""Get the randomness summary"""
	if not exists(fnRandomnessSummary):
		output = 'proof Name, file, extension, key, bytes_generated, spentTime'
		output += ', approved, pvalue, monobit_test, pvalue, frequency_within_block_test, pvalue, runs_test, pvalue, '
		output += 'longest_run_ones_in_a_block_test, pvalue, binary_matrix_rank_test, pvalue, dft_test, pvalue, '
		output += 'non_overlapping_template_matching_test, pvalue, overlapping_template_'
		output += 'matching_test, pvalue, maurers_universal_test, pvalue, linear_complexity_test, pvalue, '
		output += 'serial_test, pvalue, approximate_entropy_test, pvalue, cumulative_sums_test, pvalue, '
		output += 'random_excursion_test, pvalue, random_excursion_variant_test\n'

		with open(fnRandomnessSummary, mode='w') as file:
			file.write(output)
			file.close()
	
	with open(fnRandomnessSummary, mode='a') as file:
		file.write(argOutput)
		file.close()


def readReports(argPathSTS: str, argProof: str, argExt: str, argFile: str, 
	argSizeFile: int, argKey: str, argSpendTime: float) -> str:
	"""Read the Statistical Test Suite (STS) reports and group them in Comma 
	Separated Values (CSV)
	
	argProof     Gets the name of the test that generated the report
	argFile      Gets the name of the file used to generate the sequence 
				 analyzed by the STS and from which the report was generated
	argExt       Gets the name of the file extension used to generate the 
				 sequence analyzed by the STS and from which the report was 
				 generated
	argSizeFile	 Indicates the file size
	argKey       Gets the key used to generate the sequence analyzed by the STS
	argSpendTime Time spent generating the pseudo-random sequence, not the
				 report
	"""
	statsPath = '{}experiments/AlgorithmTesting/'.format(argPathSTS)
	output = ''
	finalScore = 0
	proof = [
			'Frequency',  # 1
			'BlockFrequency',  # 2
			'CumulativeSums',  # 3
			'Runs',  # 4
			'LongestRun',  # 5
			'Rank',  # 6
			'FFT',  # 7
			'NonOverlappingTemplate',  # 8
			'OverlappingTemplate',  # 9
			'Universal',  # 10
			'ApproximateEntropy',  # 11
			'RandomExcursions',  # 12
			'RandomExcursionsVariant',  # 13
			'Serial',  # 14
			'LinearComplexity',  # 15
			]

	for dirName in proof:
		fn = '{}/{}/stats.txt'.format(statsPath, dirName)
		cntSuccess = 0
		cntFailure = 0
		cntValues = 0
		lstPValues = []
		
		if not exists(fn):
			continue

		with open(fn, mode='r') as file:
			while True:
				buffer = file.readline()

				if not buffer:
					break

				buffer = buffer.strip()

				if 'SUCCESS' in buffer:
					cntSuccess += 1

				elif 'FAILURE' in buffer:
					cntFailure += 1

				if ('\tp_value = ' in buffer
						or ' p_value = ' in buffer
						or ' p-value = ' in buffer
						or '\tp_value1 = ' in buffer
						or '\tp_value2 = ' in buffer):
					pValue = float(buffer[-8:])
					lstPValues.append(pValue)

				elif (buffer[-6:].isdigit() and '.' == buffer[-7:-6]
						and not '=' in buffer):
					pValue = float(buffer[-8:])
					lstPValues.append(pValue)

					if pValue >= 0.01:
						cntSuccess += 1

					else:
						cntFailure += 1

				elif 'SUCCESS' in buffer[-8:] or 'FAILURE' in buffer[-8:]:
					# print(buffer[-15:-8])
					pValue = float(buffer[-15:-8])
					lstPValues.append(pValue)

				elif len(buffer) == 80:
					pValue = float(buffer[60:69])
					lstPValues.append(pValue)

		# print(dirName, lstPValues)
		cntValues = cntSuccess + cntFailure
		score = round(cntSuccess / cntValues, 2)
		# print(score)
		finalScore += score
		pValueAverage = round(sum(lstPValues) / float(len(lstPValues)),2)
		output += ',{},{}'.format(pValueAverage, score)

	output = '{},{},{},{},'.format(argProof, argFile, argExt, argSizeFile) \
			+ '{},{},{}{}'.format(argKey, argSpendTime, finalScore, output)

	return finalScore, output


def tests(argFunction,
          argCrypt: bool = False,
          argRenewCryptByCycle: bool = False,
          argXOR: bool = False) -> None:
	"""Test function

	Build pseudorandom sequences and obtain metrics

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
	argId = ''
	argId += 'XOR' if argXOR else ""
	argId += 'Crypt' if argCrypt else ""
	argId += 'RegenCrypt' if argRenewCryptByCycle else ""

	reportsDir = 'data/{}{}'.format(argFunction.__name__, argId)
	fnPerformance = 'data/performance_{}.csv'.format(argFunction.__name__)

	print('\nTest for {}'.format(argFunction.__name__))

	# Get the key files and place them in the directory for tests
	getDownloadAndTruncateFiles()
	copySTS(reportsDir)
	files = FilesNames()

	keys = getKeys()

	# Create working directory, if not exists
	if not exists(reportsDir):
		makedirs(reportsDir)

	requiredInBytes = sizeOfTheStream // 8
	requiredInBytes4Performance = sizeOfTheStream4Performance

	# Keys and files are mixed to facilitate their processing in parallel,
	# thus blocking by mutual exclusion is difficult to follow the same
	# sequence of tasks
	files.shuffleFiles()
	shuffle(keys)

	# Build pseudorandom sequences
	for cFn in files.scrollFileNames():
		for cKey in keys:
			cfs = Circular_File_Synthesizer((files.eval(),))
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

			if argCrypt:
				cfs.crypt()

			if argRenewCryptByCycle:
				cfs.crypt()
				cfs.renewCryptByCycle()
			# END Modes

			cfs.jumpPos(cfs.readIntHash % len(cfs.data))

			# Build output file name
			fnMask = files.mask(argId, cKey)
			fnReport = files.maskReport(argId, cKey)

			if not exists(fnMask) and not exists(fnReport):
				# When you create it, prevent another thread from taking it
				with open(fnMask, mode='wb') as file:
					file.close()

				print("Build: {}".format(fnMask))
				outputData = b''

				startTime = time()

				# Note: argFunction is a generator or iterator
				# in other words, is a equivalent at lazy function
				for data in argFunction(cfs, key,
                                        requiredInBytes4Performance):
					outputData += data

				spentTime = time() - startTime

				# Dump the data
				with open(fnMask, mode='wb') as file:
					file.write(outputData[:requiredInBytes])
					file.close()

				# BEGIN Record performance
				myLockFile(fnPerformance)

				if not exists(fnPerformance):
					with open(fnPerformance, mode='a') as file:
						file.write("function, mode, cFn, idKey, bytes generated, spentTime\n")
						file.close()

				with open(fnPerformance, mode='a') as file:
					file.write("{}, {}, {}, {}, {}, {} \n".format(
						argFunction.__name__, argId, cFn, bytes2int(cKey),
						requiredInBytes4Performance, spentTime))
					file.close()

				myUnlockFile(fnPerformance)
				# END Record performance

				print('\t{} s'.format(spentTime))

				# Verify if there is a stop request
				stopRequest()

			# Evaluate randomness
			if not exists(fnReport):
				# TODO Corregir parametros que se agregaron
				spentTime = evalRandomnesOfFile(fnReport, reportsDir)

				output = ''
				myLockFile(fnPerformance)

				with open(fnRandomnessSummary, mode='w') as file:
					file.write(output)
					file.close()

				myUnlockFile(fnPerformance)

				# Verify if there is a stop request
				stopRequest()

	print('Complete {}'.format(argId))


if __name__ == '__main__':
	"""Example of use"""
    # This block is to be able to use the sample code at the end of the file
    # External libraries
	from sys import path as syspath
	from os import system
	from os.path import basename
	from os.path import splitext
	import platform

	syspath.append('..')

	# Project libraries

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')
