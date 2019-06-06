##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         testVectors.py
# Purpose:      Vectores de prueba de permutaciones para el pseudo-cubo de Rubik
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 06/03/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


import os
import struct
from random import randint
from gfbpp import cellEval
from gfbpp import GFBPP
from permutations import Chi
from permutations import chi
from permutations import dseta
from permutations import mu
from permutations import eta
from permutations import fi
from permutations import iota
from permutations import ipsilon
from permutations import lambda_
from permutations import ni
from permutations import omega
from permutations import rho
from permutations import sigma
from permutations import xi


#   F U N C I O N E S   A U X I L I A R E S   #


def csv2Tex():
	""" Transforma un archivo CSV en TEX """
	import os
	import shutil

	for fn in os.listdir('csv'):
		if fn[len(fn) - 4: ] == ".csv":
			filename = fn[0: len(fn) - 4]
			output = '\\hline\n'

			with open('csv/%s' % fn, mode='r') as file:
				head = file.readline()
				output += head
				output += '\\hline\n' + file.read() + '\\hline\n'
				file.close()

			output = output.replace(',', ' & ')
			output = output.replace('\n', ' \\\\\n')
			output = output.replace('\\hline \\\\\n', '\\hline\n')
			output = output.replace('$\\hline', '\\hline')
			output = output.replace(';', ',')

			output = '\\begin{tabular}{|%s|}\n' % \
					('c' * len(head.split(','))) + output
			output += '\\end{tabular}'

			with open('csv/%s' % filename + '.tex', mode='w') as file:
				file.write(output)
				file.close()


def printFile(fileName, myMode, *data):
	""" Genera un archivo CSV con los datos porporcionados
		- fileName  Nombre del archivo
		- myMode    Modo de escritura en el archivo ("w" o "a")
		- *data     Datos que se van a escribir
	"""
	with open('csv/%s.csv' % fileName, mode=myMode) as file:
		first = True

		for d in data:
			if first:
				file.write('%s' % d)
				first = False

			else:
				file.write(',%s' % d)

		file.write('\n')
		file.close()


#   V E C T O R E S   D E   P R U E B A   #


def testPerm():
	""" Vectores de pueba para las permutaciones propuestas """

	def makeTurns(fn, name, cube, operations):
		""" Genera vectores de pueba para las permutaciones "ni" y "eta"
			- fn         Funcion que se va a ejecutar
			- name       Nombre de la funcion que se va a ejecutar
			- cube       Datos que se van a permutar
			- operations Veces que se va a permutar
		"""
		fileName = 'csv%s' % name
		printFile(fileName, 'a', '$\\hline')
		printFile(fileName, 'a', '$X \\leftarrow$', '\\texttt{0x%0128X}' % cube)
		tmp = cube

		for op in operations:
			tmp = fn(tmp, op)
			printFile(fileName, 'a', '$X \\leftarrow %s$\\gls{%s}$(X)$' % \
					((op,'')[op==1], name.lower()),
					'$\\texttt{0x%0128X}$' % tmp)

	def makePer512(fn, name, cube, parameters, operations):
		""" Genera vectores de pueba para las permutaciones "lambda", "fi",
		"dseta" y "mu"
			- fn         Funcion que se va a ejecutar
			- name       Nombre de la funcion que se va a ejecutar
			- cube       Datos que se van a permutar
			- parameters Parametros de la permutacion
			- operations Veces que se va a permutar
		"""
		fileName = 'csv%s' % name
		printFile(fileName, 'a', '$\\hline')
		printFile(fileName, 'a', '$X \\leftarrow$', '\\texttt{0x%0128X}' % cube)
		tmp = cube

		for par in parameters:
			for op in operations:
				tmp = fn(tmp, par)
				printFile(fileName, 'a',
						'$X \\leftarrow$ \\gls{%s}$(X;0x%02X)$' \
						% (name.lower(), par), '$\\texttt{0x%0128X}$' % tmp)

	def makePer64(fn, name, segment, parameter, operations):
		""" Genera vectores de pueba para las permutaciones "ipsilon", "xi",
		"rho", "iota", "sigma" y "omega"
			- fn         Funcion que se va a ejecutar
			- name       Nombre de la funcion que se va a ejecutar
			- segment    Datos que se van a permutar
			- parameters Parametros de la permutacion
			- operations Veces que se va a permutar
		"""
		fileName = 'csv%s' % name
		printFile(fileName, 'a', '$\\hline')
		printFile(fileName, 'a', '$X \\leftarrow$',
				'\\texttt{0x%016X}' % segment)
		tmp = segment

		for op in operations:
			tmp = fn(tmp, parameter)
			printFile(fileName, 'a', '$X \\leftarrow$ \\gls{%s}$(X;%s)$' \
					% (name.lower(), parameter), '$\\texttt{0x%016X}$' % tmp)

	# Giros (ni eta)
	head = "\\textbf{Operaci\\'on}, \\textbf{Vector}"
	printFile('csvNi', 'w', head)
	printFile('csvEta', 'w', head)
	maxVect = 3
	operations = [1,1,1,1, 2,2,2, 3,3,3,3,3]
	vectors = [randint(1, 2 ** 512 - 1) for i in range(maxVect)]

	for test in vectors:
		makeTurns(ni, 'Ni', test, operations)
		makeTurns(eta, 'Eta', test, operations)

	# x Columnas (lambda_ fi)
	head = "\\textbf{Operaci\\'on}, \\textbf{Vector}"
	printFile('csvLambda', 'w', head)
	printFile('csvFi', 'w', head)
	maxVect = 5
	parameters = [15, 240]
	operations = [1,1,1,1]
	vectors = [randint(1, 2 ** 512 - 1) for i in range(maxVect)]

	for test in vectors:
		makePer512(lambda_, 'Lambda', test, parameters, operations)
		makePer512(fi, 'Fi', test, parameters, operations)

	# NOT (dseta)
	printFile('csvDseta', 'w', head)
	printFile('csvMu', 'w', head)
	maxVect = 10
	parameters = [15, 240]
	operations = [1,1]
	vectors = [randint(1, 2 ** 512 - 1) for i in range(maxVect)]

	for test in vectors:
		makePer512(dseta, 'Dseta', test, parameters, operations)
		makePer512(mu, 'Mu', test, parameters, operations)

	# x Segmento (ipsilon xi rho iota sigma omega)
	printFile('csvIota', 'w', head)
	printFile('csvRho', 'w', head)
	printFile('csvOmega', 'w', head)
	printFile('csvSigma', 'w', head)
	printFile('csvXi', 'w', head)
	printFile('csvIpsilon', 'w', head)

	maxVect = 4
	parameters = [1,8]
	operations = [1 for i in range(8)]
	vectors = [randint(1, 2 ** 64 - 1) for i in range(maxVect)]

	for test in vectors:
		makePer64(iota, 'Iota', test, parameters[0], operations)
		makePer64(rho, 'Rho', test, parameters[0], operations)
		makePer64(omega, 'Omega', test, parameters[1], operations)
		makePer64(sigma, 'Sigma', test, parameters[1], operations)
		makePer64(xi, 'Xi', test, parameters[1], operations)
		makePer64(ipsilon, 'Ipsilon', test, parameters[1], operations)


def testCellEval(argFileName, argRange):
	""" Construte los vectores de pueba para los las reglas de celulas
	- argFileName  Nombre del archivo en que se van a almacenar los resultados
	- argRange     Rango que se va a evaluar
	"""
	with open('csv/%s' % argFileName, mode='w') as file:
		States = (0b111, 0b110, 0b101, 0b100, 0b011, 0b010, 0b001, 0b000)

		# Encabezados
		output = '\\textbf{Rule}'
		for state in States:
			output += ',$\\textbf{%s}_2$' % "{:03b}".format(state, '#b')
		output += ',\\textbf{Rule}'
		for state in States:
			output += ',$\\textbf{%s}_2$' % "{:03b}".format(state, '#b')
		file.write('%s\n' % output)

		# Tablas
		for rule in range(argRange[0], argRange[1]):
			output = '$\\textbf{%s}_{10}$ $(\\textbf{%s}_2)$' % (rule,
					"{:08b}".format(rule, '#b'))

			for near in States:
				output += ',%s' % cellEval(rule, near)

			if rule % 2 == 1:
				file.write('%s\n' % output)

			else:
				file.write('%s,' % output)

		file.close()


def testAC(argFileName, argPhi, argGenerations):
	""" Evalua las reglas de un AC
	- argFileName    Nombre del archivo en que se van a almacenar los resultados
	- argPhi         Regla que se va a evaluar
	- argGenerations Generaciones que se van aevaluar
	"""
	# Definicion
	size = 32
	bFmt = '{:0%sb}' % size
	gf = GFBPP(size)
	gf.setDelta(0x10000)
	output = '$\\phi$,\\textbf{g},\\textbf{bin($\\Delta$)}, ' + \
			'\\textbf{hex($\\Delta$)}\n'

	# Fijar Regla para la celula
	for s in gf.S:
		s.Psi = [argPhi]

	# Evolucion
	for i in range(argGenerations + 1):
		output += '%s,%s,\\texttt{0b%s},\\texttt{0x%0.8X}\n' % \
				(argPhi, gf.g, bFmt.format(gf.getDelta(), '#b'), gf.getDelta())
		gf.evolve()

	with open('csv/%s' % argFileName, mode='w') as file:
		file.write(output)
		file.close()


def main():
	print("Construyendo vectores de prueba")
	testPerm()
	testCellEval('csvCellEval1.csv', [0, 64])
	testCellEval('csvCellEval2.csv', [64, 128])
	testCellEval('csvCellEval3.csv', [128, 192])
	testCellEval('csvCellEval4.csv', [192, 256])
	testAC('csvAC30.csv', 30, 32)
	testAC('csvAC135.csv', 135, 32)
	csv2Tex()
	print("Vectores terminados")


if __name__ == '__main__':
    main()
