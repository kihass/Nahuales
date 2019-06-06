##!/usr/bin/python2
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         testVectors.py
# Purpose:      Evaluacion de aleatoriedad para el GFBPP
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 06/03/14"
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


def bin2Str(argData, argWidth = 0):
	""" Convierte un numero en su representacion binaria, en la longitud
	solicitada
	   - argData.  Numero binario
	   - argWidth.  Cantidad de bits requeridos
	retorna la cadena binaria """
	fmt = '{:0%sb}' % argWidth
	return fmt.format(argData)


def rndTestBin(argMaxSize = 0):
	""" Pruebas de aleatoriedad
	- argMaxSize    Tamano maximo en caso de que no se cuente con suficiente
					poder de procesamiento para evaluar todo el archivo binario
	"""
	print 'Iniciando pruebas de aleatoriedad'

##	for fn in os.listdir('data'):
##		if fn[len(fn) - 4: ] == '.bin':
##			filename = 'data/%s' % fn[0: len(fn) - 4]
	for iTest in range(1, 1000 + 1):
		for iCriteria in range(1, 4 + 1):
			filename = 'data/Criterio%s_%04i' % (iCriteria, iTest)

			if not os.path.isfile('%s.randomness' % filename):
				with open('%s.randomness' % filename, mode='a') as file:
					file.close()

				print 'Analizando %s ' % filename + '\n%s' % datetime.now()
				sizeFile = os.path.getsize('%s.bin' % filename)
				print 'Tamano real:\t', sizeFile, 'bytes'

				with open('%s.bin' %  filename, 'rb') as file:
					size = (argMaxSize, sizeFile)[argMaxSize == 0]
					skip = sizeFile - size
					print 'Analizando:\t', size, 'bytes'
					file.seek(0)
					output = ''

					for b in range(sizeFile):
						data = file.read(1)

						if b >= skip:
							byte = struct.unpack('>B', data)[0]
							output += bin2Str(byte, 8)

					ALL(filename, output, '%s,%s' % (filename[13:14],
							filename[15:]))

					file.close()


def entropyBinStream(argStream):
	""" Calcula la entropia de un arreglo de flujos de datos binarios.  Los
	parametros son:
		  - argStream: Cadena binaria
		retorna el valor calculado de la entropia """
	# Cuenta los 0's y 1's
	myCont = [argStream.count('0'), argStream.count('1')]
	mySum = sum(myCont)

	if mySum > 0:
		entropy = float(0)

		for i in range(2):
			ph = myCont[i] / float(mySum)

			try:
				entropy -= ph * math.log(ph,2)

			except:
				print 'exception'
				pass

		return entropy

	else:
		return 0


def ALL(argFileName, argBin, argTag):
	""" Ejecuta todos los test disponibles """
	tests = (
			(entropyBinStream, 'entropy'),					# 0
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
##			(linearcomplexitytest, 'linearcomplexitytest'),	# 10 mucho tiempo
##			(serialtest, 'serialtest'),	# 11 mucho tiempo
##			(aproximateentropytest, 'aproximateentropytest'),	# 12 mucho tiempo
			(cumultativesumstest, 'cumultativesumstest'),	# 13
##			(randomexcursionstest, 'randomexcursionstest'),	# 14
##			(randomexcursionsvarianttest, 'randomexcursionsvarianttest')#,	# 15
##			(cumultativesumstestreverse, 'cumultativesumstestreverse')		# 16
			)
	conjRes = []
	extras = []

	for iFn in range(len(tests)):
		fn = tests[iFn][0]
		result = fn(argBin)
		print '%s %s: \t%s' % (datetime.now(), tests[iFn][1], result)

		if type(result) == type([]):
			extras.append(result[:])
			tmpList = []

			for i in result:
				if math.isnan(i):
					tmpList.append(0)

				else:
					tmpList.append(i)

			result = float(sum(tmpList)) / len(tmpList)

		conjRes.append(result)

	avg = sum(conjRes) / len(conjRes)
	conjRes.append(avg)

	outRes = '%s' % conjRes
	outRes = outRes.replace('[', '').replace(']', '').replace(' ', '')
	outRes = outRes.replace("'", '')

	print '\nCalificacion final:', avg

	if argTag != '':
		print 'Guardando cambios\n'
		with open('%s.randomness' % argFileName, mode = 'w') as file:
			file.write('%s,%s\n' % (argTag, outRes))
			for xtr in extras:
				file.write('%s\n' % xtr)
			file.close()

	return conjRes


def main():
	bytes4Eval = 1024 * 512
	rndTestBin(bytes4Eval)


if __name__ == '__main__':
    main()
