##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MyECC.py
# Purpose:     Implementación parcial de Criptografía de Curvas Elípticas
#
# Author:      ISC. Carlos Enrique Quijano Tapia
#
# Created:     22/10/2013
# Copyright:   (c) Kihass 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------


import pickle
import os


def gcd(a,b):
	""" Máximo comun divisor por el algoritmo extendido de Euclides """
	if b == 0:
		return a
	else:
		return gcd(b, a % b)


def egcd(a, b):
	""" Encuentra el máximo comun divisor aplicando el algoritmo extendido de
	Euler.
	http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python"""
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)


def multiplicativeInverse(z, Zp):
	""" Encuentra z^-1 aplicando el algoritmo extendido de Euler """
	g, t, y = egcd(z, Zp)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		inv = t % Zp
		if (inv * z) % Zp == 1:
			return inv
		else:
			print('Euler falló para', z, '-', Zp)
			return self.multiplicativeInverseSlow(z, Zp)


def multiplicativeInverseSlow(z, Zp):
	""" Encuentra z^-1 por fuerza bruta """
	t = 1
	while not (t * z) % Zp == 1:
		t += 1
	return t


class ECC(object):

	Zp = None   # Campo Base
	E = None	# Polinomio
	Ϭ = (-1, -1)    # Punto al infinito
	rp = [Ϭ]	# Conjunto de puntos racionales
	orders = [] # Diccionario de ordenes del los puntos racionales
	preQ = []   # Listado de precálculos de Q
	addTable = None # Tabla de adición
	α = []	# Listado de generadores


	def findRationalPoints(self, E, Zp, Ϭ = (-1, -1)):
		""" Encuentra los puntos racionales de una curva """
		self.Ϭ = Ϭ
		self.rp = [Ϭ]
		self.Zp = Zp
		self.E = E
		rp = self.rp
		print('\nCurva elíptica: y^2 = %sx^3 + %sx^2 + %sx + %s   |  Z_p = %s' %
				(E[3],E[2],E[1],E[0], Zp))

		# Evalua todos los valores de X en el campo
		for x in range(Zp):
			z = (E[3] * x ** 3 + E[2] * x ** 2 + E[1] * x + E[0]) % Zp

			# Evalua todos los valores de Y en el campo
			for y in range(Zp):
				y2 = (y ** 2) % Zp

				# Agrega los puntos racionales que existen
				if y2 == z:
					rp.append((x,y))

		if len(rp) < 30:
			print('Puntos racionales: ', rp, ' |G| = ', len(rp))
		else:
			print('Demasiados puntos racionales, |G| = ', len(rp))

		# Crea diccionario de orden de puntos racionales
		self.orders = dict([(i, None) for i in self.rp])


	def isRationalPoints(self, E, Zp, P):
		""" Comprueba que P es un punto racional """
		x = P[0]
		y = P[1]
		z = (E[3] * x ** 3 + E[2] * x ** 2 + E[1] * x + E[0]) % Zp
		y2 = (y ** 2) % Zp
		if y2 == z:
			return True
		else:
			return False


	def addition(self, P, Q):
		""" Función de aditiva """
		Zp = self.Zp
		Ϭ = self.Ϭ
		a = self.E[1]
		α = 0

		# Sí Ϭ == (P or Q)
		if P == Ϭ or Q == Ϭ:
			if P == Ϭ:
				return Q
			else:
				return P
		else:
			# P == ~Q
			if P == (Q[0], (-Q[1]) % Zp):
				return (-1,-1)
			else:
				# Calcula los valores α
				if P != Q:
					α = ((Q[1] - P[1]) % Zp) * \
							multiplicativeInverse((Q[0] - P[0]) % Zp, Zp)
				else:
					α = ((3 * P[0] ** 2 + a) % Zp) * \
							multiplicativeInverse((P[1] + Q[1]) % Zp, Zp)
				# Calcula el punto
				x_3 = (α ** 2 - P[0] - Q[0]) % Zp
				y_3 = (α * (P[0] - x_3) - P[1]) % Zp
				return (x_3, y_3)


	def buildAddTable(self):
		""" Construye la tabla aditiva """
		rp = self.rp

		# Construye matriz
		self.addTable = [[self.addition(rp[i], rp[j]) for i in range(len(rp))]
				for j in range(len(rp))]
		addTable = self.addTable

		# Muestra resultados
		print('\nEl grupo:')
		for i in addTable:
			print(i)

		# Muestra el orden de todos los puntos
		print('\nOrden de puntos:')
		for i in rp:
			print(i, ' \t', self.order(i))


	def order(self, P):
		""" Encuentra el orden de un punto """
		Ϭ = self.Ϭ
		found = P
		myOrder = 1

		while found != Ϭ:
			myOrder += 1
			found = self.addition(found,P)

		return myOrder


	def orderFast(self, P):
		""" Búsca sí anteriormente ya se ha calculado y guardado el orden del
		numero solicitado, en caso contrario lo calcula y almacena, para uso
		futuro """

		# Comprueba que el diccionario de ordenes corresponda al caso
		if len(self.orders) != len(self.rp) \
				or len(self.rp) == 0 \
				or len(self.orders) == 0:
			if len(self.rp) == 0:
				self.findRationalPoints(self.E, self.Zp, self.Ϭ)
			print('Creando diccionario de orders')
			self.orders = dict([(i, None) for i in self.rp])

		# Sí no se ha calculado, lo calcula y guarda
		if self.orders[P] == None:
			self.orders[P] = self.order(P)

			self.svPreCalc()
		return self.orders[P]


	def fndQ(self, d, P):
		""" Busca el punto el valor Q dado Q = dP """
		Q = None
##		print(bin(d)) # DEBUGG
		# Buscando el bit mas significativo
		bitMore = 0
		while d >= 2 ** bitMore:
			bitMore += 1

		contBitMore = bitMore

##		cont = 1  # DEBUGG
##		self.preQ = []  # DEBUGG
		while contBitMore > 0:
			# Extraer bit
			bit = (d >> contBitMore - 1) & 0b1
##			output = ''  # DEBUGG

			# Exponenciación rápida
			if bit == 1:
				if contBitMore < bitMore:
##					print('-' * 8) # DEBUGG
##					output += '%s,' % (cont * 2 + 1)  # DEBUGG
					Q = self.addition(Q, Q)
##					output += '"2(%sP) = %s",' % (cont, Q)  # DEBUGG
##					cont *= 2  # DEBUGG
##					print('2X + 1 = ', Q) # DEBUGG
					Q = self.addition(Q, P)
##					output += '"%sP + P = %s"' % (cont, Q)  # DEBUGG
##					cont += 1  # DEBUGG
##					print('X + P = ', Q) # DEBUGG
				else:
##					print('-' * 8) # DEBUGG
##					output += '%s,' % cont  # DEBUGG
					Q = self.addition(P, self.Ϭ)
##					output += '"P = (%s, %s)"' % (Q[0], Q[1])  # DEBUGG
##					print('P = ', Q) # DEBUGG
			else:
##				print('-' * 8) # DEBUGG
##				output += '%s,' % (cont * 2)  # DEBUGG
				Q = self.addition(Q, Q)
##				output += '"2(%sP) = %s"' % (cont, Q)  # DEBUGG
##				cont *= 2  # DEBUGG
##				print('2P = ', Q) # DEBUGG
##			self.preQ.append(output)  # DEBUGG
			contBitMore -= 1

##		print(P, Q) # DEBUGG
		return Q


	def fndQSlow(self, d, P):
		""" Verificación de resultado de Q=dP lenta (usar sólo para comprobar
		resultados) """
		Q = self.addition(self.Ϭ, self.Ϭ)  # P
		for i in range(d):  # d - 1
			Q = self.addition(Q, P)
		return Q


	# Esta parte sólo es para guardar y cargas datos calculados


	def calcMassOrders(self):
		""" Calcula masivamente el orden de los elementos faltantes """
		print('\nCalculamos el orden masivamente:')
		contSv = 0
		cont = 0
		lenRP = len(self.rp)
		for i in self.orders.keys(): # DEBUGG
			if self.orders[i] == None: # DEBUGG
	##			print('Calculando orden de', i) # DEBUGG
				self.orders[i] = self.order(i) # DEBUGG
				contSv += 1
			if contSv == 200:
				self.svPreCalc()
				contSv = 0
				print(datetime.now(), '\t', cont, 'de', lenRP)
			cont += 1
		self.calcGen()
		self.svPreCalc()


	def calcGen(self):
		""" Calcula los generadores """
		self.α = []
		size = len(self.rp)
		myMax = 0
		distinctOrders = []
		for i in self.orders.keys():
			if self.orders[i] == size:
				self.α.append(i)
			if self.orders[i] > myMax:
				myMax = self.orders[i]
			if self.orders[i] not in distinctOrders:
				distinctOrders.append(self.orders[i])
		distinctOrders.sort()
##		print('Encontramos', len(self.α), 'generadores.  El máximo orden fue',
##				myMax)
		print('Encontramos los siguientes ordenes:', distinctOrders)



	def getFilename(self):
		""" Obtiene el nombre del archivo """
		E = self.E
		filename = '%sx^3_%sx^2_%sx_%s' % (E[3], E[2], E[1], E[0]) + \
				'-[Zp=%s].pickle' % self.Zp
		return filename


	def ldPreCalc(self):
		""" Carga cálculos previos """
		E = self.E
		pathfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
				self.getFilename())
		if os.path.exists(pathfile):
##			print('Cargando cálculos previos <- "%s"' % self.getFilename())
			with open(self.getFilename(), mode='rb') as file:
				self.E = pickle.load(file)
				self.Zp = pickle.load(file)
				self.rp = pickle.load(file)
				self.orders = pickle.load(file)
##				self.α = pickle.load(file)
				file.close()
			print('\nCurva elíptica: y^2 = %sx^3 + %sx^2 + %sx + %s   |   ' %
					(E[3], E[2], E[1], E[0]), 'Z_p = %s' % self.Zp)
			return True
		else:
			return False


	def svPreCalc(self):
		""" Guarda cálculos actuales """
		print('Guardando cálculos actuales -> %s' % self.getFilename())
		with open(self.getFilename(), mode='wb') as file:
			pickle.dump(self.E, file)
			pickle.dump(self.Zp, file)
			pickle.dump(self.rp, file)
			pickle.dump(self.orders, file)
##			pickle.dump(self.α, file)
			file.close()


	def svData(self):
		""" Guarda en un archivo los datos generados """
		fileName = 'Puntos Racionales ' + self.getFilename()
		fileName = fileName.replace('pickle', 'csv')
		cont = 1
		with open(fileName, mode='w', encoding='utf-8') as file:
			file.write('Posición, punto\n')
			for i in self.rp:
				file.write('%s,"%s"\n' % (cont, i))
				cont += 1
			file.close()

##		fileName = 'Q ' + self.getFilename()
##		fileName = fileName.replace('pickle', 'csv')
##		cont = 1
##		with open(fileName, mode='w', encoding='utf-8') as file:
##			file.write('Iteración,d,,bit = 1\n')
##			for i in self.preQ:
##				file.write('%s,%s\n' % (cont, i))
##				cont += 1
##			file.close()


def main():
	pass

if __name__ == '__main__':
    main()
