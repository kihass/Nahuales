##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         randTestVectors.py
# Purpose:      Vectores de prueba para el gfbpp
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 06/03/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


import os
import struct
import math #TODO
from random import randint
from gfbpp import cellEval
from gfbpp import GFBPP
from testVectors import csv2Tex


#   F U N C I O N E S   A U X I L I A R E S   #


def chStyleCsv():
	""" Da formato al archivo csvGFBPP.tex """
	changes = [['csvGFBPP.tex', '|cccc|', '|c|l|c|c|'],
			['detailsAVG.tex', '|ccccc|', '|l|c|c|c|c|']]
	read = ''

	for ch in changes:
		with open('csv/%s' % ch[0], mode='r') as file:
			read = file.read()
			file.close()

		read = read.replace(ch[1], ch[2])

		with open('csv/%s' % ch[0], mode='w') as file:
			file.write(read)
			file.close()


#   V E C T O R E S   D E   P R U E B A   #


def testGFBPP(argMin, argMax):
	""" """
	fileSize = 1024 * 1024 # Tamano en bytes
	size = 16
	maxPsi = 16
	minPsi = 5
	offset = size // 2
	criteria = [[],
			[],  # Control
			[30, 75, 86, 89, 101, 135, 149], # Clase III
			[30, 90, 105, 150, 165, 86, 101, 153, 39], # Seredynski2003
			[rule for rule in range(1, 256)] # Indiscriminado
			]

	for test in range(argMin, argMax + 1):

		# Control
		if not os.path.isfile('data/Criterio1_%04i.bin' % test):
			print('Generando data/Criterio1_%04i.bin' % test)
			blocks = [randint(0,255) for i in range(fileSize)]

			with open('data/Criterio1_%04i.bin' % (test), mode='wb') as file:
				for block in blocks:
					file.write(struct.pack('>B', block))
				file.close()

		# Otros criterios
		for cr in range(2, 5):
			criId = 'data/Criterio%s_%04i' % (cr, test)

			if not os.path.isfile('%s.bin' % criId):
				print('\nGenerando %s.bin' % criId)
				cRules = criteria[cr]
				rules = [[] for i in range(size)]
				delta = 2 ** (size // 2)

				# Fijar cantidades de reglas y reglas escogidas al azar para la
				# celula
				for iRul in range(len(rules)):
					sizePsi = randint(minPsi, maxPsi)
					rules[iRul] = [cRules[randint(0, len(cRules) - 1)] \
							for i in range(sizePsi)]

				print('Reglas que seran usadas:')
				for rul in rules:
					print(rul)

				# Construir el archivo binario
				mkGFBin(criId, size, rules, delta, fileSize, offset)


def mkGFBin(argId, argSize, argRules, argDelta, argSizeFile, argOffset):
	""" Construye un generador de flujo que a su vez genera un archivo binario
	mediante su flujo, ademas de un archivo CSV con las reglas usadas
	- argId         Identificador o nombre del archivo de salida
	- argSize       Cantidad de celulas de GF
	- argRules      Conjunto de reglas
	- argSizeFile   Tamano del archivo de salida
	- argOffset     Generaciones iniciales omitidas antes de empezar a construir
                    el binario
	"""
	gf = GFBPP(argSize)
	gf.setDelta(argDelta)
	output = ''
	pos = 0
	blocks = []

	# Fijando reglas
	for s in gf.S:
		s.Psi = argRules[pos][:]
		output += '%s\n' % s.Psi
		pos += 1

	# Evolucion
	for ev in range(argOffset + argSizeFile * 8 // argSize + 1):
		gf.evolve()

		if ev > argOffset:
			data = gf.getDelta()

			for iBlock in range(argSize // 8):
				blocks.append((data >> (iBlock * 8)) & 0xFF)

	# Escribiendo archivo de reglas
	with open('%s.rules' % argId, mode = 'w') as file:
		file.write(output)
		file.close()

	# Escribiendo archivo binario
	with open('%s.bin' % argId, mode = 'wb') as file:
		for block in blocks:
			file.write(struct.pack('>B', block))

		file.close()


def randAbstract(digits):
	""" Recopila los resultados de las pruebas realizadas y hace un resumen
	- digits  Digitos a los que seran redondeados los resultados del resumen """
	print('Recopilando informacion de las pruebas realizadas')
	denominator = 10 ** digits
	results = {}
	outRand = ''
	outRandomness = ''
	tests = [
		['shannonentropy', [],[],[],[]],   # 0
		['monobitfrequencytest', [],[],[],[]],   # 1
		['blockfrequencytest', [],[],[],[]],   # 2
		['runstest', [],[],[],[]],   # 3
		['longestrunones10000', [],[],[],[]],   # 4
		['binarymatrixranktest', [],[],[],[]],   # 5
		['spectraltest', [],[],[],[]],   # 6
		['nonoverlappingtemplatematchingtest', [],[],[],[]],   # 7
		['overlappingtemplatematchingtest', [],[],[],[]], # 8
		['maurersuniversalstatistictest', [],[],[],[]],   # 9
##		['linearcomplexitytest', [],[],[],[]],   # 10 mucho tiempo
##		['serialtest', [],[],[],[]],   # 11 mucho tiempo
##		['aproximateentropytest', [],[],[],[]],   # 12 mucho tiempo
		['cumultativesumstest', [],[],[],[]],   # 13
##		['randomexcursionstest', [],[],[],[]],   # 14
##		['randomexcursionsvarianttest', [],[],[],[]],   # 15
##		['cumultativesumstestreverse', [],[],[],[]],   # 16
##		['lempelzivcompressiontest', [],[],[],[]]
		]

	for i in range(0, denominator + 1):
		results[i / denominator] = {1:0, 2:0, 3:0, 4:0}

	for fn in os.listdir('data'):
		if fn[len(fn) - 11: ] == '.randomness':
			filename = 'data/%s' % fn

			with open(filename, mode = 'r') as file:
				data = file.readline().split(',')
				vCriteria = int(data[0])
				vEval = int(data[1])
				vRes = float(data[len(data) - 1])
				tmp = '%s' % data
				tmp = tmp.replace('[','').replace(']','')
				tmp = tmp.replace(' ','').replace("'",'').replace('\\n','')
				outRandomness += '%s\n' % tmp
				outRand += '%s,%s,%s\n' % (vCriteria, vEval, vRes)
				results[round(vRes, digits)][vCriteria] += 1

				for tst in range(2, len(data) - 1):
					if not math.isnan(float(data[tst])):
						tests[tst - 2][vCriteria].append(float(data[tst]))

				file.close()

	with open('csv/randomnes.csv', mode = 'w') as file:
		file.write('%s' % outRandomness)
		file.close()

	with open('csv/rand.csv', mode = 'w') as file:
		file.write('%s' % outRand)
		file.close()

	print('Construyendo el resumen')

	with open('csv/randAbstract.csv', mode='w') as file:
		file.write("aleatoriedad,Criterio 1,Criterio 2,Criterio 3,Criterio 4\n")

		for i in range(0, denominator):
			file.write('%s' % (i / denominator))
			file.write(',%s,%s' % (results[i / denominator][1],
					results[i / denominator][2]))
			file.write(',%s,%s\n' % (results[i / denominator][3],
					results[i / denominator][4]))

		file.close()

	with open('csv\detailsAVG.csv', mode = 'w') as file:
		file.write('\\textbf{Test},\\textbf{Criterio 1},\\textbf{Criterio 2}' +\
		',\\textbf{Criterio 3},\\textbf{Criterio 4}\n')
		for tst in range(len(tests)):
			tit = tests[tst][0]
			avg1 = sum(tests[tst][1]) / len(tests[tst][1])
			avg2 = sum(tests[tst][2]) / len(tests[tst][2])
			avg3 = sum(tests[tst][3]) / len(tests[tst][3])
			avg4 = sum(tests[tst][4]) / len(tests[tst][4])
			file.write('%s,%.3f,%.3f,%.3f,%.3f\n' % (tit, avg1, avg2, avg3,
					avg4))
		file.close()


def avgGFBPP():
	""" Construye la tabla de promedios """
	results = {1:{'alias': "Control (funci\\'on random)", 'data':[]},
			2:{'alias': "Reglas conocidas", 'data':[]},
			3:{'alias': "Sugeridas\\cite{Seredynski2003}", 'data':[]},
			4:{'alias': "Indiscriminadamente", 'data':[]}}

	print('Construyendo tabla de resultados')

	with open('csv/rand.csv', mode = 'r') as file:
		while True:
			data = file.readline()

			if not data:
				break

			data = data.split(',')
			vCriteria = int(data[0])
			vRes = float(data[2])
			results[vCriteria]['data'].append(vRes)

		file.close()

	with open('csv/csvGFBPP.csv', mode='w') as file:
		file.write("\\textbf{Criterio}, \\textbf{Alias}, ")
		file.write("\\textbf{Promedio}, \\textbf{Simulaciones}\n")

		for cr in range(1, 4 + 1):
			file.write("%s, %s" % (cr, results[cr]['alias']))
			file.write(", %.3f" % (sum(results[cr]['data']) / \
					len(results[cr]['data'])))
			file.write(", %s\n" % len(results[cr]['data']))

		file.close()


def main():
	import sys
	print("Construyendo vectores de prueba aleatorios")

	if '--build' in sys.argv:
		testGFBPP(1, 1000)

	else:
		randAbstract(2)
		avgGFBPP() # csvGFBPP.csv
		csv2Tex()
		chStyleCsv()

	print("Vectores terminados")


if __name__ == '__main__':
    main()
