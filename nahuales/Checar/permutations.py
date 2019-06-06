##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         permutations.py
# Purpose:      'Algoritmos de permutacion para cubos y segmentos'
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 06/03/14"
__project__ = 	'DduC'
__doc__ = 		'Libreria de permutaciones para el pseudo-cubo de Rubik'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


from random import randint


def coord2Dpos(i, j):
	""" Convierte las coordenadas bidimensionales a la posicion lineal
	equivalente
	- i     Eje de Coordenadas X
	- j     Eje de coordenadas Y
	"""
	return i + 8 * j


def coord2pos(i, j, k):
	""" Convierte las coordenadas bidimensionales a la posicion lineal
	equivalente
	- i     Eje de Coordenadas X
	- j     Eje de coordenadas Y
	- k     Eje de coordenadas Z
	"""
	return i + 8 * j + 8 * 8 * k


def chi(cube, cutting, tilt):
	""" Extraccion de segmento del cubo
	- cube     Cubo de 512 bits
	- cutting  Filas o columnas que se van a extraer
	- tilt     Inclinacion horizontal (0) u vertical (1)
	"""
	tilt %= 2
	cutting %= 8
	segment = 0

	if tilt == 0:  # Horizontal
		cube = ni(cube, 1)

	else:  #  Vertical
		cube = eta(cube, 3)

	segment = (cube >> 64 * cutting) & 0xFFFFFFFFFFFFFFFF

	return segment


def Chi(cube, segment, cutting, tilt):
	""" Integracion de segmento con cubo
	- cube     Cubo de 512 bits
	- segment  Segmento que se va a agregar
	- cutting  Fila o columna que se van a integrar [0, ..., 7]
	- tilt     Inclinacion vertical (0) u horizontal (1)
	"""
	tilt %= 2
	cutting %= 8
	newCube = 0

	if tilt == 0:
		cube = ni(cube, 1)

	else:
		cube = eta(cube, 3)

	for glide in range(8):
		if glide == cutting:
			newCube |= segment << cutting * 64

		else:
			newCube |= ((cube >> glide * 64) & 0xFFFFFFFFFFFFFFFF) << glide * 64

	if tilt == 0:
		newCube = ni(newCube, 3)

	else:
		newCube = eta(newCube, 1)

	return newCube


def ni(cube, turns):
	""" Permutacion girar cubo verticalmente
	- cube     Cubo de 512 bits
	- turns    Vueltas
	"""
	turns %= 4

	if turns == 0:
		return cube

	else:
		newCube = 0

		for k in range(8):
			for j in range(8):
				pos = coord2pos(0, j, k)
				glide = 0

				if turns == 1:
					glide = coord2pos(0, k, 7 - j)

				elif turns == 2:
					glide = coord2pos(0, 7 - j, 7 - k)

				elif turns == 3:
					glide = coord2pos(0, 7 - k, j)

				newCube |= ((cube >> pos) & 0xFF) << glide

		return newCube


def eta(cube, turns):
	""" Permutacion girar cubo horizontalmente
	- cube     Cubo de 512 bits
	- turns    Vueltas
	"""
	turns %= 4

	if turns == 0:
		return cube

	else:
		newCube = 0

		for k in range(8):
			for j in range(8):
				for i in range(8):
					pos = coord2pos(i, j, k)
					glide = 0

					if turns == 1:
						glide = coord2pos(7 - k, j, i)

					elif turns == 2:
						glide = coord2pos(7 - i, j, 7 - k)

					elif turns == 3:
						glide = coord2pos(k, j, 7 - i)

					newCube |= ((cube >> pos) & 0b1) << glide

		return newCube


def ipsilon(segment, glide):
	""" Permutacion corrimiento vertical circular reptante
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	glide %= 64

	if glide == 0:
		return segment

	else:
		return auxIpsilon(sigma(auxIpsilon(segment), glide))


def auxIpsilon(segment):
	""" Ordena segmento en patron ipsilon
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	newSegment = segment & 0x5555555555555555

	for row in range(8):
		newSegment |= ((segment >> row * 8) & 0xAA) << (7 - row) * 8

	return newSegment


def xi(segment, glide):
	""" Permutacion corrimiento horizontal circular reptante
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	glide %= 64

	if glide == 0:
		return segment

	else:
		return auxXi(omega(auxXi(segment), glide))


def auxXi(segment):
	""" Ordena segmento en patron xi
	- segment  Segmento de 64 bits
	"""
	newSegment = segment & 0x00FF00FF00FF00FF

	for glide in [1,3,5,7]:
		newSegment |= (segment >> (glide * 8) & 0xFF) << (7 - glide + 1) % 8 * 8

	return newSegment


def iota(segment, glide):
	""" Permutacion corrimiento horizontal circular independiente
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	glide %= 8

	if glide == 0:
		return segment

	else:
		newSegment = 0

		for pos in range(8):
			mask = 0xFF << pos * 8
			newSegment |= (segment & mask) >> glide & mask
			newSegment |= (segment & mask) << (8 - glide) & mask

		return newSegment


def rho(segment, glide):
	""" Permutacion corrimiento vertical circular independiente
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	glide %= 8
	if glide == 0:
		return segment
	else:
		glide *= 8
		newSegment = segment >> glide | (segment & (2 ** glide - 1)) << \
				(64 - glide)

		return newSegment


def omega(segment, glide):
	""" Permutacion corrimiento horizontal circular zigzagueante
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	glide %= 64

	if glide == 0:
		return segment

	else:
		newSegment = segment >> glide | (segment & (2 ** glide - 1)) << \
				(64 - glide)

		return newSegment


def sigma(segment, glide):
	""" Permutacion corrimiento vertical circular zigzagueante
	- segment  Segmento de 64 bits
	- glide    Deslizamiento
	"""
	glide %= 64

	if glide == 0:
		return segment

	else:
		hGlide = glide // 8
		vGlide = glide % 8

		# Vertical
		newSegment = (segment << vGlide * 8) & 0xFFFFFFFFFFFFFFFF
		tmp = segment >> (8 - vGlide) * 8

		for row in range(vGlide):
			aux = (tmp >> row * 8) & 0xFF
			aux = ((aux << 1) | (aux >> 7)) & 0xFF
			newSegment |= aux << row * 8

		segment = newSegment

		# Horizontal
		newSegment = 0
		tmp = segment

		for row in range(8):
			aux = (tmp >> row * 8) & 0xFF
			aux = ((aux << hGlide) | (aux >> (8 - hGlide))) & 0xFF
			newSegment |= aux << row * 8

		return newSegment


def bitChanges(byte):
	""" Obtiene un arreglo con las nuevas posiciones
	- byte     byte que se va a procesar
	"""
	alternate = []
	changes = [None for i in range(8)]

	for bit in range(8):
		if byte >> bit & 0b1 == 1:
			alternate.append(bit)

		else:
			changes[bit] = bit

	for bit in range(len(alternate)):
		if bit + 1 == len(alternate):
			changes[alternate[bit]] = alternate[0]

		else:
			changes[alternate[bit]] = alternate[bit + 1]

	return changes


def lambda_(cube, byte):
	""" Permutacion de columnas
	- cube     Cubo de 512 bits
	- byte     byte que se va a procesar

	NOTA: lambda es una palabra reservada en python asi que se renombro
	"""
	if byte == 0:
		return cube

	else:
		newCube = 0
		glide = 0
		# Las siguientes dos lineas son porque la representacion hexadecimal de
		# la mascara es muy larga (128 caracteres)
		mask = 0x01010101010101010101010101010101
		mask |= mask << 128 | mask << 256 | mask << 384

		changes = bitChanges(byte)

		for pos in range(8):
			glide = changes[pos] - pos

			if glide >= 0:
				newCube |= (cube & mask << pos) << glide

			else:
				glide *= -1
				newCube |= (cube & mask << pos) >> glide

		return newCube


def fi(cube, byte):
	""" Permutacion de filas
	- cube     Cubo de 512 bits
	- byte     byte que se va a procesar
	"""
	if byte == 0:
		return cube

	else:
		newCube = 0
		glide = 0
		# Las siguientes dos lineas son porque la representacion hexadecimal de
		# la mascara es muy larga (128 caracteres)
		mask = 0x00000000000000FF00000000000000FF
		mask |= mask << 128 | mask << 256 | mask << 384

		changes = bitChanges(byte)

		for pos in range(8):
			glide = changes[pos] - pos

			if glide >= 0:
				newCube |= (cube & mask << pos * 8) << glide * 8

			else:
				glide *= -1
				newCube |= (cube & mask << pos * 8) >> glide * 8

		return newCube


def dseta(cube, byte):
	""" Negacion de columnas
	- cube     Cubo de 512 bits
	- byte     byte que se va a procesar
	"""
	if byte == 0:
		return cube

	else:
		newCube = 0
		nCube = ~cube
		# Las siguientes dos lineas son porque la representacion hexadecimal de
		# la mascara es muy larga (128 caracteres)
		mask = 0x01010101010101010101010101010101
		mask |= mask << 128 | mask << 256 | mask << 384

		for pos in range(8):
			if byte >> pos & 0b1 == 1:
				newCube |= nCube & mask << pos

			else:
				newCube |= cube & mask << pos

		return newCube


def mu(cube, byte):
	""" Negacion de Filas
	- cube     Cubo de 512 bits
	- byte     byte que se va a procesar
	"""
	if byte == 0:
		return cube

	else:
		newCube = 0
		nCube = ~cube
		# Las siguientes dos lineas son porque la representacion hexadecimal de
		# la mascara es muy larga (128 caracteres)
		mask = 0x00000000000000FF00000000000000FF
		mask |= mask << 128 | mask << 256 | mask << 384

		for pos in range(8):
			if byte >> pos & 0b1 == 1:
				newCube |= nCube & mask << pos * 8

			else:
				newCube |= cube & mask << pos * 8

		return newCube

