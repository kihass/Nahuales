#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Coding Primes

Encode prime numbers in binary and csv files. These numbers were obtained from
here:
	primes.utm.edu
	and 
	https://static.bigprimes.net/archive/one-billion-primes.7z.torrent
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
import datetime
from os.path import exists
from os import listdir
from os import remove
from os import system
import platform
import struct

lstPrimes = []
itemsInList = 0
fIndex = 0
lastNumber = 4294967291
rangesFile = 'rangesOfListOfPrimesNumbers.py'
groupSize = 100000


def openOriginalFile(fn, argUtm=True):
	flaEnd = False
	global lstPrimes
	global itemsInList
	global fIndex
	global lastNumber
	global groupSize

	# Import prime lists
	with open(fn, 'r') as file:
		if argUtm:
			# Ignore first line
			buffer = file.readline()

		while True:
			buffer = file.readline()
				
			if not buffer:
				break

			if len(buffer) > 1:
				# Clear the string
				buffer = buffer.strip()

				buffer = buffer.replace('\n', ' ')
				buffer = buffer.replace('\t', ' ')

				while buffer.find('  ') != -1:
					buffer = buffer.replace('  ',' ')

				buffer = buffer.split(' ')

				for num in buffer:
					num = int(num)
					lstPrimes.append(num)
					itemsInList += 1

					if itemsInList >= groupSize or num == lastNumber:
						save()
						itemsInList = 0
						lstPrimes = []
						fIndex += 1

						if num == lastNumber:
							flaEnd = True
							break

			if flaEnd:
				break

		file.close()


def save():
	global rangesFile
	global lstPrimes
	global fIndex

	print('{}  {}'.format(datetime.datetime.now(), fIndex))
	minLocal = float('inf')
	maxLocal = 0

	with open('data/primes{}.bin'.format(fIndex), mode='wb') as file:
		for num in lstPrimes:
			file.write(struct.pack('<I', num))
			minLocal = num if num < minLocal else minLocal
			maxLocal = num if minLocal < num else minLocal
	
		file.close()
	
	initialString = ''

	if not exists(rangesFile):
		initialString = 'lstPrimesNumRanges = [\n'

	with open(rangesFile, mode='a') as file:
		file.write('{}\t({},{},{},{}),\n'.format(initialString, fIndex,
                minLocal, maxLocal, len(lstPrimes)))
		file.close()

	# with open('data/primes{}.csv'.format(fIndex), mode='w') as file:
	# 	cnt = 1
	# 	for num in lstPrimes:
	# 		file.write('{}{}'.format(num, ',' if cnt % 10 else '\n'))
	# 		cnt += 1

	# 	file.close()

	print('{}  last:{}'.format(datetime.datetime.now(), maxLocal))


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

	# for fNumber in range(1, 50+1):
	# 	fn = 'data/originals/primes{}.txt'.format(fNumber)

	# 	if exists(fn):
	# 		print('{}  {}'.format(datetime.datetime.now(), fn))

	# 	openOriginalFile(fn, True)
	#	remove(fn)

	fn = 'data/originals/one-billion-primes.txt'
	openOriginalFile(fn, False)
	# remove(fn)
	
	with open(rangesFile, mode='a') as file:
		file.write(']\n')
		file.close()
