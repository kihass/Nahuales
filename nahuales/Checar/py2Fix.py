##!/usr/bin/python2
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         testVectors.py
# Purpose:      Corregir funciones cuya implementación previa no funciono
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 05/10/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


import os
import struct
import math
from random import randint
from datetime import datetime
from nist.randtest import monobitfrequencytest
from nist.randtest import blockfrequencytest
from nist.randtest import runstest
from nist.randtest import longestrunones10000
from nist.randtest import binarymatrixranktest
from nist.randtest import spectraltest
from nist.randtest import nonoverlappingtemplatematchingtest
from nist.randtest import overlappingtemplatematchingtest
from nist.randtest import maurersuniversalstatistictest
from nist.randtest import linearcomplexitytest
from nist.randtest import serialtest
from nist.randtest import aproximateentropytest
from nist.randtest import cumultativesumstest
from nist.randtest import randomexcursionstest
from nist.randtest import randomexcursionsvarianttest
from nist.randtest import cumultativesumstestreverse
from nist.randtest import lempelzivcompressiontest
from py2EvalRnd import bin2Str
from py2EvalRnd import entropyBinStream


def rndAdjustmentBin(argMaxSize, argWorks):
	""" Correccion de pruebas de aleatoriedad
	- argMaxSize    Tamano maximo en caso de que no se cuente con suficiente
					poder de procesamiento para evaluar todo el archivo binario
	"""
	cntTest = 1
	print 'Iniciando pruebas de aleatoriedad'
	lstFiles = []

	for fn in os.listdir('data'):
		if fn[len(fn) - 4: ] == '.bin':
			filename = 'data/%s' % fn[0: len(fn) - 4]

			if os.path.isfile('%s.randomness' % filename):
				lstFiles.append(filename)

	while len(lstFiles) > 0:
		filename = lstFiles.pop(randint(0, len(lstFiles) - 1))
		results = []

		with open('%s.randomness' % filename, mode='r') as file:
			results = file.readline()
			results = results.split(',')
			file.close()

		print 'Analizando %s (%s/4000)' % (filename, cntTest) + \
				'\n%s' % datetime.now()
		cntTest += 1

		with open('%s.bin' %  filename, 'rb') as file:
			size = file.seek(0,2)
			size = (argMaxSize, size)[argMaxSize == 0]
			print size, 'bytes'
			file.seek(0)
			output = 0
			cont = 0

			for b in range(size):
				data = file.read(1)
				byte = struct.unpack('>B', data)[0]
				output |= byte << cont * 8
				cont += 1

			fixIt(filename, output, True,
					'%s,%s' % (filename[13:14], filename[15:]), size, argWorks,
					results)

			file.close()


def fixIt(argFileName, argBin, argShow, argTag, argMaxBytes, argWorks,
		argResults):
	tests = ((entropyBinStream, 'entropy'),		# 0
			(monobitfrequencytest, 'monobitfrequencytest'),	# 1
			(blockfrequencytest, 'blockfrequencytest'),		# 2
			(runstest, 'runstest'),							# 3
			(longestrunones10000, 'longestrunones10000'),	# 4
			(binarymatrixranktest, 'binarymatrixranktest'),	# 5
			(spectraltest, 'spectraltest'),					# 6
			(nonoverlappingtemplatematchingtest,
				'nonoverlappingtemplatematchingtest'),		# 7
			(overlappingtemplatematchingtest,
				'overlappingtemplatematchingtest'),			# 8
			(maurersuniversalstatistictest, 'maurersuniversalstatistictest'),# 9
##			(linearcomplexitytest, 'linearcomplexitytest'),	# 10
##			(serialtest, 'serialtest'),						# 11
##			(aproximateentropytest, 'aproximateentropytest'),	# 12
##			(cumultativesumstest, 'cumultativesumstest'),	# 13
##			(randomexcursionstest, 'randomexcursionstest'),	# 14
##			(randomexcursionsvarianttest, 'randomexcursionsvarianttest'),	# 15
##			(cumultativesumstestreverse, 'cumultativesumstestreverse'),		# 16
##			(lempelzivcompressiontest, 'lempelzivcompressiontest')			# 17
			)
	stream = bin2Str(argBin)
	changed = False

	for iFn in argWorks:
		fn = tests[iFn][0]
		result = 0.0
		argResults[iFn + 2] = float(argResults[iFn + 2])

		if argResults[iFn + 2] < argWorks[iFn] or \
				math.isnan(argResults[iFn + 2]):
			changed = True

			result = fn(stream)
			print '%s %s: \t%s -> %s' % (datetime.now(), tests[iFn][1],
					argResults[iFn + 2], result)

			if iFn in [11,14,15]:
				tmpList = []

				for i in result:
					if math.isnan(i):
						tmpList.append(0)

					else:
						tmpList.append(i)

				result = float(sum(tmpList)) / len(tmpList)

			argResults[iFn + 2] = result

	sumRes = 0

	for i in range(len(argResults) - 1):
		if i >= 2:
			argResults[i] = float(argResults[i])
			sumRes += argResults[i]

	avg = sumRes / (len(argResults)- 3)
	argResults[len(argResults) - 1] = avg

	argResults = '%s' % argResults
	argResults = argResults.replace('[', '').replace(']', '').replace(' ', '')
	argResults = argResults.replace("'", '')

	if argTag != '' and changed:
		print 'Guardando cambios'
		with open('%s.randomness' % argFileName, mode='w') as file:
			file.write('%s\n' % argResults)
			file.close()

	if argShow:
		print 'Calificacion final:', avg, '\n'

	return argResults


def main():
	argMaxSize = 1024 * 2
	argWorks = {11: 0.5}
	rndAdjustmentBin(argMaxSize, argWorks)


if __name__ == '__main__':
    main()
