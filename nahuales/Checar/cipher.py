##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         cipher.py
# Purpose:      Libreria de permutaciones para el pseudo-cubo de Rubik
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 06/03/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


from math import ceil
from gfbpp import GFBPP, acGenEval
from random import randint
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
import permutations
import hashlib
import struct
import types
import sys


# * * * * * * * * * *  Funciones y clases auxiliares  * * * * * * * * * * * * *

class FILE_PARAM(object):
	name = ''
	size = 0
	pos = 0


class GF(object):
	parameters = GFBPP(0)


class GF_PARAM(object):
	pos = 0


class MESSAGE_PARAM(object):
	data = 0
	size = 0
	cubes = 0


class MD(object):
	active = True
	name = ''
	size = 0


class VAR(object):
	fk = FILE_PARAM()
	gfParam = GF_PARAM()
	m = MESSAGE_PARAM()


class CONFIG_PARAM(object):
	initEvolutions = 0


class CONFIG(object):
	gfParam = CONFIG_PARAM()
	maxIterations = None
	md = MD()
	tokens = None
	tokens3Parameters = ['iota', 'ipsilon', 'omega', 'rho', 'sigma', 'xi']


class PARAM(object):
	crypt = False
	decrypt = False
	fk = FILE_PARAM()
	inputFile = None
	k = None
	m = MESSAGE_PARAM()
	outputFile = None
	dependsOfKey = False  # Al depender de la llave imposibilita el diseno

def size(data):
	""" Obtiene el tamano de los datos
	- data  Datos a partir de los cuales se va obtener el hash.  Tipos de
            datos soportados (str, int, file) """
	typ = type(data)

	if typ == type(''):
		return len(data)

	elif typ == type(0b0):
		bits = 0

		while True:
			if 2 ** bits > data:
				break

			bits += 1

		return ceil(bits / 8)

	elif str(typ) == "<class '_io.BufferedReader'>":
		tmpSize = data.seek(0,2)
		data.seek(0)
		return tmpSize

	else:
		print(typ, 'no esta admitido')
		exit(1)


def sha512(data, salt=None):
	""" Simplificacion para usar sha512 de forma transparente
	- data  Datos a partir de los cuales se va obtener el hash.  Tipos de
            datos soportados (str, int, bytes)
	- salt  Sal con la que se va a condimentar el hash """
	if type(data) == type(''):
		data = bytes(data, 'utf-8')

	elif type(data) == type(0):
		data = bytes(data)

	if salt != None:
		data = data + bytes(salt)

	myHash = hashlib.sha512()
	myHash.update(data)
	return int(myHash.hexdigest(), 16)


def sha256(data, salt=None):
	""" Simplificacion para usar sha256 de forma transparente
	- data  Datos a partir de los cuales se va obtener el hash.  Tipos de
            datos soportados (str, int, bytes)
	- salt  Sal con la que se va a condimentar el hash """
	if type(data) == type(''):
		data = bytes(data, 'utf-8')

	elif type(data) == type(0):
		data = bytes(data)

	if salt != None:
		data = data + bytes(salt)

	myHash = hashlib.sha256()
	myHash.update(data)
	return int(myHash.hexdigest(), 16)


# * * * * * * * * * * * *  Implementacion de algoritmos * * * * * * * * * * * *

def loadConfig():
	""" Carga configuracion del cifrado """
	myHelp = 'Cifrado inspirado en cubos de Rubik, resistente a ataques de ' + \
			'fuerza bruta.\n\ncipher.py {-c|-d} [-dk | s=POSITION] ' + \
			'[t=TOKENS] i=FILENAME o=FILENAME [k=KEY] fk=FILENAME\n'
	myHelp += '\n   -?\t\tMuestra esta ayuda.'
	myHelp += '\n   -c\t\tCifra un archivo.'
	myHelp += '\n   -d\t\tDescifra un archivo.'
	myHelp += '\n   -dk\t\tIndica que la posicion inicial en fk depende de' + \
			' la llave.'
	myHelp += '\n   -ps\t\tOmite usar archivo md, incluye o extrae (segun ' + \
			'sea el caso)\n\t\tel tamano del archivo en el archivo cifrado.'
	myHelp += '\n   fk=FILE\tNombre del archivo llave que se va a usar.'
	myHelp += '\n   if=FILE\tNombre del archivo que se va a cifrar.'
	myHelp += '\n   k=KEY\tLlave de cifrado.'
	myHelp += '\n   m=ITERATIONS\tCantidad maxima de iteraciones que se ' + \
			'pueden procesar \n\t\t(numero de 4 bytes como maximo).  '
	myHelp += '\n   of=FILE\tNombre del archivo de salida cifrado.'
	myHelp += '\n   s=POSITION\tPosicion inicial en fk.'
	myHelp += '\n   t=TOKENS\tListado de tokens que se van a usar, ' + \
			'separados por comas.  \n\n\t\tEjemplo:\n' + \
			'\t\tt=dseta,mu,eta,fi,iota,ipsilon,lambda,ni,omega,rho,sigma,xi'

	if '-?' in sys.argv:
		print(myHelp)
		exit(0)

	# Valores por defecto
	config.maxIterations = 32
	config.tokens = ['dseta', 'mu', 'eta', 'fi', 'iota', 'ipsilon', 'lambda',
			'ni', 'omega', 'rho', 'sigma', 'xi']
	config.gfParam.initEvolutions = 0
	parameters.fk.name = None
	parameters.fk.size = 0
	parameters.k = None
	parameters.m.data = 0
	parameters.m.size = None

	# Lectura de parametros
	parameters.dependsOfKey = (False, True)['-dk' in sys.argv]
	config.md.active = (True, False)['-ps' in sys.argv]

	if '-c' in sys.argv:
		parameters.crypt = True
		parameters.decrypt = False

	else:
		if '-d' in sys.argv:
			parameters.crypt = False
			parameters.decrypt = True

	for arg in sys.argv:

		if len(arg) >= 3:

			if arg[ : 3] == 'fk=':
				parameters.fk.name = arg[3 : ]

				with open(parameters.fk.name, 'rb') as file:
					parameters.fk.size = size(file)
					file.close()

			elif arg[ : 3] == 'if=':
				parameters.inputFile = arg[3 : ]

				# Abrir archivo y ponerlo en M
				with open(parameters.inputFile, 'rb') as file:
					parameters.m.size = size(file)

					for byte in reversed(range(parameters.m.size)):
						read = struct.unpack('>B', file.read(1))[0]
						parameters.m.data |= read << byte * 8

					file.close()

			elif arg[ : 2] == 'k=':
				parameters.k = arg[2 : ]

			elif arg[ : 2] == 'm=':
				config.maxIterations = int(arg[2 : ])

			elif arg[ : 3] == 'of=':
				parameters.outputFile = arg[3 : ]

			elif arg[ : 2] == 's=':
				config.gfParam.initEvolutions = int(arg[2 : ])

			elif arg[ : 2] == 't=':
				tokens = arg[2 : ].split(',')

				for iTok in tokens:
					if iTok not in config.tokens:
						print('Error fatal, el token indicado "%s"' % iTok + \
								' no esta implementado')
						exit(1)

				config.tokens = tokens


def activeBits(byte):
	""" Obtiene un arreglo con los bytes activos
	- byte   Byte que se va a convertir en arreglo """
	if byte == 0:
		return []

	else:
		positions = []

		for bit in range(8):
			if byte >> bit & 0b1 == 1:
				positions.append(bit)

		return positions


def cFk(nonZero = False):
	""" Lee un byte de la siguiente posicion del archivo llave circular """
	file = open(var.fk.name, 'rb')
	read = 0

	while True:
		var.fk.pos %= var.fk.size
		file.seek(var.fk.pos)
		# La siguiente linea se debe a que python es un lenguaje de tipado
		# dinamico y es equivalente a read = file.read(1) en otros lenguajes
		read = struct.unpack('>B', file.read(1))[0]
		var.fk.pos += 1

		if nonZero:
			if 0 < read < 255:
				break
		else:
			break

	file.close()

	return read


def initGF(size, Delta):
	""" Construccion del generador de flujo
	- size   Celulas del GF
	- Delta  Conjunto de estados iniciales """
	gf.parameters = GFBPP(size)
	gf.parameters.setDelta(Delta)

	for s in gf.parameters.S:
		s.Psi = []

		for phi in range(cFk(True)):
			s.Psi.append(cFk(True))


def getParameter():
	""" Obtiene un byte del generador de flujo """
	if (var.gfParam.pos + 1) * 8 >= gf.parameters.size:
		var.gfParam.pos %= gf.parameters.size
		acGenEval(gf.parameters)

	read = (gf.parameters.getDelta() >> var.gfParam.pos) & 0xFF
	var.gfParam.pos += 1
	return read


def fToken(instruction):
	""" Encuentra la instruccion en la tabla de Tokens """
	token = instruction % len(config.tokens)
	return config.tokens[token]


def mkInstructions(m):
	""" Construye las instrucciones de cifrado """
	# Evoluciones iniciales del generador de flujo de parametros
	for ev in range(config.gfParam.initEvolutions):
		acGenEval(gf.parameters)

	instructions = [[] for iCube in range(var.m.cubes)]

	for iCube in range(var.m.cubes):
		totalInstructions = (getParameter() << 24 | getParameter() << 16 | \
				getParameter() << 8 | getParameter()) % config.maxIterations + 1

		for localInstructions in range(totalInstructions):
			token = fToken(cFk())
			param = []

			if token in config.tokens3Parameters:
				param.append(getParameter())
				param.append(getParameter())
				param.append(getParameter())

			else:
				param.append(getParameter())

			instructions[iCube].append((token, param))

	return instructions


def interpret(token, cube, param):
	""" Interprete de tokens de cifrado """
	if token == 'dseta':
		return dseta(cube, param[0])

	elif token == 'mu':
		return mu(cube, param[0])

	elif token == 'eta':
		if parameters.decrypt:
			param[0] = -param[0] % 4

		return eta(cube, param[0])

	elif token == 'ni':
		if parameters.decrypt:
			param[0] = -param[0] % 4

		return ni(cube, param[0])

	elif token == 'fi':
		if parameters.decrypt:
			rounds = len(activeBits(param[0])) - 1

			for rnd in range(rounds):
				cube = fi(cube, param[0])

			return cube

		else:
			return fi(cube, param[0])

	elif token == 'lambda':
		if parameters.decrypt:
			rounds = len(activeBits(param[0])) - 1

			for rnd in range(rounds):
				cube = lambda_(cube, param[0])

			return cube

		else:
			return lambda_(cube, param[0])


	elif token == 'iota':
		if parameters.decrypt:
			param[0] = -param[0] % 64

		for bit in activeBits(param[1]):
			segment = chi(cube, 2 ** bit, param[2])
			segment = iota(segment, param[0])
			cube = Chi(cube, segment, 2 ** bit, param[2])

		return cube


	elif token == 'ipsilon':
		if parameters.decrypt:
			param[0] = -param[0] % 64

		for bit in activeBits(param[1]):
			segment = chi(cube, 2 ** bit, param[2])
			segment = ipsilon(segment, param[0])
			cube = Chi(cube, segment, 2 ** bit, param[2])

		return cube


	elif token == 'omega':
		if parameters.decrypt:
			param[0] = -param[0] % 64

		for bit in activeBits(param[1]):
			segment = chi(cube, 2 ** bit, param[2])
			segment = omega(segment, param[0])
			cube = Chi(cube, segment, 2 ** bit, param[2])

		return cube

	elif token == 'rho':
		if parameters.decrypt:
			param[0] = -param[0] % 64

		for bit in activeBits(param[1]):
			segment = chi(cube, 2 ** bit, param[2])
			segment = rho(segment, param[0])
			cube = Chi(cube, segment, 2 ** bit, param[2])

		return cube

	elif token == 'sigma':
		if parameters.decrypt:
			param[0] = -param[0] % 64

		for bit in activeBits(param[1]):
			segment = chi(cube, 2 ** bit, param[2])
			segment = sigma(segment, param[0])
			cube = Chi(cube, segment, 2 ** bit, param[2])

		return cube

	elif token == 'xi':
		if parameters.decrypt:
			param[0] = -param[0] % 64

		for bit in activeBits(param[1]):
			segment = chi(cube, 2 ** bit, param[2])
			segment = xi(segment, param[0])
			cube = Chi(cube, segment, 2 ** bit, param[2])

		return cube

	else:
		print('Error fatal, token "%s" no implementado' % token)
		exit(1)


def cypher(m, k, fk):
	""" Cifrado
	- m   Mensaje que se va a cifrar
	- k   Llave que se va a autilizar
	- fk  Archivo llave que se va a utilizar """
	var.m = m
	var.fk = fk
	prevCube = 0

	# Construir cubos con mensaje en claro
	if config.md.active:
		var.m.cubes = ceil(var.m.size / 64)

		with open('%s.details' % parameters.outputFile, 'w') as file:
			file.write('%s\n' % var.m.size)
			file.close()

	else:
		var.m.cubes = ceil((var.m.size + 8) / 64)
		# Agregar en los ultimos 8 bytes el tamano del mensaje
		var.m.data = var.m.data | var.m.size << (var.m.cubes * 512 - 64)

	# Iniciar Generador de Flujo
	initGF(256, sha256(k))

	# Construir conjunto de instrucciones por cubo
	sk = mkInstructions(var.m.data)

	mask = 2 ** 512 - 1
	maskXOR = 0
	lstCubes = [iCube for iCube in range(var.m.cubes)]
	lstNewOrder = []

	salt = bytes("", 'utf-8')

	file = open(var.fk.name, 'rb')

	for byte in range(var.fk.size):
		salt += file.read(1)

	file.close()

	for iCube in range(var.m.cubes):
		# Construye mascara XOR para el cubo
		salt += bytes(k, 'utf-8') + struct.pack('<B', getParameter())
		maskXOR |= sha512(salt) << iCube * 512
		# Asigna nueva posicion
		lstNewOrder.append(lstCubes.pop(getParameter() % len(lstCubes)))

	# Enmascara cubos
	var.m.data ^= maskXOR
	mt = 0

	for iCube in range(var.m.cubes):
		cube = (var.m.data >> iCube * 512) & mask

		# XOR con cubo previo
		if iCube > 0:
			cube ^= prevCube

		# Interpreta el conjunto de instrucciones que le corresponde
		for token, param in sk[iCube]:
			cube = interpret(token, cube, param)

		prevCube = cube

		# Construccion del mensaje cifrado
		mt |= cube << lstNewOrder[iCube] * 512

	return mt


def descypher(m, k, fk):
	""" Descifrado
	- m   Mensaje que se va a descifrar
	- k   Llave que se va a autilizar
	- fk  Archivo llave que se va a utilizar """
	var.m = m
	var.fk = fk

	# Construir cubos con mensaje cifrado
	var.m.cubes = ceil(var.m.size / 64)

	# Iniciar Generador de Flujo
	gf = initGF(256, sha256(k))

	# Construir conjunto de instrucciones por cubo
	sk = mkInstructions(var.m.data)

	mask = 2 ** 512 - 1
	maskXOR = 0
	lstCubes = [iCube for iCube in range(var.m.cubes)]
	lstNewOrder = []

	salt = bytes("", 'utf-8')

	file = open(var.fk.name, 'rb')

	for byte in range(var.fk.size):
		salt += file.read(1)

	file.close()

	for iCube in range(var.m.cubes):
		# Construye mascara XOR para el cubo
		salt += bytes(k, 'utf-8') + struct.pack('<B', getParameter())
		maskXOR |= sha512(salt) << iCube * 512
		# Asigna nueva posicion
		lstNewOrder.append(lstCubes.pop(getParameter() % len(lstCubes)))

	mt = 0

	for iCube in reversed(range(var.m.cubes)):
		cube = (var.m.data >> lstNewOrder[iCube] * 512) & mask

		# Interpreta el conjunto de instrucciones que le corresponde
		for token, param in reversed(sk[iCube]):
			cube = interpret(token, cube, param)

		# XOR con cubo previo
		if iCube > 0:
			cube ^= (var.m.data >> (lstNewOrder[iCube - 1]) * 512) & mask

		mt |= cube << iCube * 512

	# Enmascara cubos
	mt = mt ^ maskXOR

	# Construye mensaje en claro
	if config.md.active:
		with open('%s.details' % parameters.inputFile, 'r') as file:
			var.m.size = int(file.readline())
			file.close()

	else:
		# Extraer de los ultimos 8 bytes el tamano del mensaje
		prevSize = var.m.size
		var.m.size = mt >> (var.m.cubes * 512 - 64)

		if not (prevSize - 512 < var.m.size < prevSize + 512):
			print('\nError fatal al descifrar, los parametros, archivo llave o',
					'llave no pueden generar el archivo solicitado. ',
					'Verifiquelos.')
			exit(1)

	return mt & 2 ** (var.m.size * 8) - 1


config = CONFIG()
gf = GF()
parameters = PARAM()
var = VAR()


def main():
	loadConfig()
	mt = 0
	mask = 2 ** 512 - 1

	if parameters.dependsOfKey:
		parameters.fk.pos = sha256(parameters.k) & 0xFFFF

	if parameters.crypt:
		mt = cypher(parameters.m, parameters.k, parameters.fk)

		# Poner en archivo de salida
		with open(parameters.outputFile, 'wb') as file:
			for iCube in reversed(range(var.m.cubes)):
				cube = (mt >> iCube * 512) & mask

				for byte in reversed(range(64)):
					data = (cube >> byte * 8) & 0xFF
					file.write(struct.pack('>B', data))

			file.close()

	elif parameters.decrypt:
		mt = descypher(parameters.m, parameters.k, parameters.fk)

		# Poner en archivo de salida
		with open(parameters.outputFile, 'wb') as file:
			for byte in reversed(range(var.m.size)):
				data = (mt >> byte * 8) & 0xFF
				file.write(struct.pack('>B', data))

			file.close()

	# Limpiar contrasena de la memoria
	parameters.k = randint(1, 9e99)

if __name__ == '__main__':
	main()

