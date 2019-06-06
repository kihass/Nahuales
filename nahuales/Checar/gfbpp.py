##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         gfbpp.py
# Purpose:      'Generador de Flujos Pseudo-aleatorios Personalizable'
__author__ =    'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ =   "$Version: 0 Revision: 0 Since: 20/05/14"
__project__ =   'DduC'
__copyright__ = '(c) Kihass 2014'
__licence__ =   'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


def cellEval(phi, near):
	""" Evaluacion de Celula
	- phi   Conjunto de reglas
	- near  Vecindad
	"""
	if (phi >> near) & 0b1 == 1:
		return 1

	else:
		return 0


def cellNear(S, n):
	""" Estados vecinos de la celula
	- S     Conjunto de celulas
	- n     Indice de la celula de la que se buscara la vecindad
	"""
	sizeS = len(S)  # Agregado por optimizacion
	near = 0

	# bit 0
	if n == 0:
		near |= S[sizeS - 1].delta

	else:
		near |= S[n - 1].delta

	# bit 1
	near |= S[n].delta << 1

	# bit 2
	if n == sizeS - 1:
  		near |= S[0].delta << 2

	else:
		near |= S[n + 1].delta << 2

	return near


def acGenEval(ac):
	""" Evaluacion de generacion del AC
	- ac    Automata Celular"""
	ac.g += 1
	Delta = 0

	for s in ac.S:
		near = cellNear(ac.S, s.n)
		phi = calRule(ac.g, s)
		Delta |= cellEval(phi, near) << s.n

	ac.setDelta(Delta)


def calRule(g, s):
	""" Evaluacion de generacion del AC para GFBPP
	- g     Generacion
	- s     Celula
	"""
	return s.Psi[g % len(s.Psi)]


class CELL(object):
	n = None  # Posicion de la celula
	delta = None  # Estado de la celula
	pdelta = None  # Estado previo de la celula
	phi = None  # Regla actual
	Psi = []  # Conjunto de reglas

	def __init__(self, n):
		""" Celula
		- n     Indice de la celula
		"""
		self.n = n


class AC(object):
	S = None # Conjunto de celulas
	Delta = None # Estado inicial del conjunto S
##	Phi = None # Conjunto de reglas
##	theta = None # Magnitud de la vecindad
##	gamma = None # Condicion frontera
	g = 0
	size = 0


	def __init__(self, size):
		""" Automata Celular
		- size      Tamano de la celula """
		self.S = [CELL(s) for s in range(size)]
		self.size = size


	def setDelta(self, Delta):
		""" Establece el conjunto de estados Delta
		- Delta     Representacion binaria del conjunto de estados
		"""
		for s in self.S:
			s.delta = (Delta >> s.n) & 1


	def getDelta(self):
		""" Devuelve el conjunto de estados Delta, como una representacion
		binaria del conjunto de estados
		"""
		Delta = 0
		for s in self.S:
			Delta |= s.delta << s.n
		return Delta


	def evolve(self):
		""" Evoluciona una generacion del AC """
		print('no implementado')


class GFBPP(AC):

	def evolve(self):
		""" Genera la evolucion del AC """
		acGenEval(self)


def test():
	""" Vector de prueba """
 	# Definicion
	size = 16
	bFmt = '{:0%sb}' % size
	gf = GFBPP(size)
	gf.setDelta(0b10000000)
	print(gf.g, '\t%s' % bFmt.format(gf.getDelta(), '#b'))
	for s in gf.S:
		s.Psi = [30]

	# Evolucion
	for i in range(16):
		gf.evolve()
		print(gf.g, '\t%s' % bFmt.format(gf.getDelta(), '#b'))


if __name__ == '__main__':
    test()
