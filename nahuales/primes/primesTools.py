#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""primesTools

Quick search tools for prime numbers. These tools are based on the use of lists of previously stored numbers
"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2019"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 22/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
# External libraries
from os import stat
import struct

# Project libraries
from rangesOfListOfPrimesNumbers import lstPrimesNumRanges


def findPosInList(argVal: int) -> tuple:
	pos = minVal = maxVal = 0
	inList = False

	for pos, minVal, maxVal, stored in lstPrimesNumRanges:
		# print(pos, minVal, argVal, maxVal)
		if argVal <= maxVal:
			if minVal <= argVal <= maxVal:
				inList = True
			else:
				pos += 1

			break

	return inList, pos


def isPrime(argVal: int):
	inList, pos = findPosInList(argVal)

	if pos >= len(lstPrimesNumRanges):
		print('{} is out of range: {}'.format(argVal, pos))
		return False
	else:
		if argVal < lstPrimesNumRanges[pos][1]:
			return False
		else:
			iterRead = readListOfPrimeNumbers(pos)

			for item in range(100000):
				primeNumber = next(iterRead)

				if argVal == primeNumber:
					return True
				elif argVal < primeNumber:
					break
			
			return False


def iteratePrimes(argSmallerThan: int=0):
	listNumber = 0

	if argSmallerThan == 0:
		listNumber = len(lstPrimesNumRanges)
		argSmallerThan = float('inf')

	else:
		inList, listNumber = findPosInList(argSmallerThan)
		listNumber += 1

	for lstNum in range(listNumber):
		for num in readListOfPrimeNumbers(lstNum):
			if num <= argSmallerThan:
				yield num
		
		# print('\nLista {}'.format(lstNum))


def iteratePrimesReverse(argSmallerThan: int=0):
	listNumber = 0
	
	if argSmallerThan == 0:
		listNumber = len(lstPrimesNumRanges)
		argSmallerThan = float('inf')

	else:
		inList, listNumber = findPosInList(argSmallerThan)
		listNumber += 1
		
	for lstNum in reversed(range(listNumber)):
		for num in readListOfPrimeNumbersReversed(lstNum):
			if num <= argSmallerThan:
				yield num

		# print('\nLista {}'.format(lstNum))


def readListOfPrimeNumbers(argListNumber: int):
	fileName = 'data/primes{}.bin'.format(argListNumber)

	with open(fileName, mode='rb') as file:
		while True:
			readNumber = file.read(4)

			if readNumber:
				readNumber = struct.unpack('<I', readNumber)[0]
				yield readNumber

			else:
				break


def readListOfPrimeNumbersReversed(argListNumber: int):
	fileName = 'data/primes{}.bin'.format(argListNumber)

	with open(fileName, mode='rb') as file:
		statinfo = stat(fileName)
		items = statinfo.st_size // 8

		for item in reversed(range(items)):
			file.seek(item * 4, 0)
			readNumber = file.read(4)

			if readNumber:
				readNumber = struct.unpack('<I', readNumber)[0]
				yield readNumber

			else:
				break


if __name__ == '__main__':
	"""Example of use"""
	# External libraries
	from os import system
	import platform

	# Project libraries
	

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	testsNumbersPrimes = [2,3,5,7,15485863,982451653]
	testsNumbersNoPrimes = [1,4,6,15485864,982451652,982451654]

	print('\nNumeros que deben ser primos')
	for num in testsNumbersPrimes:
		print('{} is prime? {}'.format(num, isPrime(num)))

	print('\nNumeros que NO deben ser primos')
	for num in testsNumbersNoPrimes:
		print('{} is prime? {}'.format(num, isPrime(num)))

	print('\nAll numbers')
	output = ''
	cnt = 0
	for num in iteratePrimes(500):
		print('{}  '.format(num), end='')

	print('\nAll numbers in reversed')
	output = ''
	cnt = 0
	for num in iteratePrimesReverse(500):
		print('{}  '.format(num), end='')
