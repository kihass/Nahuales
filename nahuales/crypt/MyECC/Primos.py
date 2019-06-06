##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        primos.py
# Purpose:     Generar listado de numeros primos
#
# Author:      ISC. Carlos Enrique Quijano Tapia
#
# Created:     03/11/2013
# Copyright:   (c) Kike 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------

import pickle
import os
import random


def bitMoreSignificative(num):
	""" Obtiene el bit mas significativo de un numero binario """
	bms = 0
	while True:
		if 2 ** bms > num:
			break
		bms += 1
	return bms


def fastExponent(a, k):
	""" Exponenciación rápida """
	A = a
	bms = bitMoreSignificative(k) - 2

	while bms >= 0:
		# A ^ 2
		A *= A

		# Extraer bit
		if (k >> bms) & 0b1 == 1:
			# A * a
			A *= a

		bms -= 1

	return A


def fastExponentZp(a, k, Zp):
	""" Exponenciación rápida """
	A = a
	bms = bitMoreSignificative(k) - 2

	while bms >= 0:
		# A ^ 2
##		A *= A
		A = (A * A) % Zp

		# Extraer bit
		if (k >> bms) & 0b1 == 1:
			# A * a
##			A *= a
			A = (A * a) % Zp

		bms -= 1

##	A %= Zp
	return A


def fermat(n, t):
	a = None
	for i in range(t):
		a = random.randint(2, n - 2)
##		r = (a ** (n - 1)) % n
##		r = fastExponent(a, n -1) % n
		r = fastExponentZp(a, n - 1, n)
		if r != 1:
			return False
	return True


class PRIME(object):

	primes = [2, 3, 5, 7, 11]
	lastCalc = 11
	limitFermat = 1

	def __init__(self):
		""" Busca números primos """
		# De existir busca el archivo de precálculos
		pathfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
				'primes.pickle')
		if os.path.exists(pathfile):
			with open('primes.pickle', mode='rb') as file:
				self.lastCalc = pickle.load(file)
				self.primes = pickle.load(file)
				file.close()


	def __del__(self):
		self.__svPrimes()
##		pass


	def isPrime(self, number):
		""" Verifiva sí un número es primo """
		# Checa sí ya se ha calculado este número primo
		if number > self.lastCalc:
##			print('Buscando primos')    # DEBUGG
			self.fndPrimes(number)

		if number in self.primes:
			return True
		else:
			return False


	def isPrimeSlow(self, number):
		flaPrime = True
		for i in range(2, number):
			if number % i == 0:
				flaPrime = False
				break

		return flaPrime


	def __calcPrime(self, number):
		""" Calcula sí el número es primo, verificando el residúo con los
		números primos anteriores conocidos"""

		flaPrime = True
		if fermat(number, self.limitFermat):
			limit = number // 2
			for i in self.primes:
				if number % i == 0:
					flaPrime = False
					break
				if i > limit:
					break
		else:
			flaPrime = False

		# Sí es primo, agregalo a la lista
		if flaPrime:
##			print(number, 'es primo')   # DEBUGG
			self.primes.append(number)
			self.lastCalc = number

		self.lastCalc = number


	def fndPrimes(self, until):
		""" Calcula los primos faltantes hasta el número pedido """
		for num in range(self.lastCalc + 2, until + 1, 2):
			self.__calcPrime(num)


	def __svPrimes(self):
		""" Salva los números primos encontrados """
		with open('primes.pickle', mode='wb') as file:
			pickle.dump(self.lastCalc, file)
			pickle.dump(self.primes, file)
			file.close()


	def svCSV(self):
		""" Guarda los números primos conocidos """
		with open('primes.csv', mode='w', encoding='utf-8') as file:
			for i in self.primes:
				file.write('%s\n' % i)
			file.close()


	def chkWithFermat(self):
		NotByFermat = []
		for i in self.primes[2:]:
			if not fermat(i, self.limitFermat):
				print('oops ->', i)
				NotByFermat.append(i)
		print('Detectados por Fermat', NotByFermat)


	def randomPrimeKBits(self, k):
		maxKBits = bitMoreSignificative(self.primes[len(self.primes) - 1])
		if k <= maxKBits:
			while True:
				p = random.randint(2 ** (k-1), 2 ** k - 1)
				if self.isPrime(p):
					return p
		else:
			while True:
				p = random.randint(2 ** (k-1), 2 ** k - 1)
				if fermat(p, 10):
					return p


def main():
	from datetime import datetime
	print('\nIniciando: ', datetime.now())
	born = datetime.now()

	prime = PRIME()

##	numero = int(2e6)
	numero = int('1' * 22, 2) + 9 * 10 ** 5
	print(len(prime.primes), 'números primos almacenados en memoria')
	print('Números primos calculados hasta', prime.lastCalc,
			hex(prime.lastCalc))
	print('Intentaremos llegar hasta:', numero)
	if prime.isPrime(numero):
		print('El numero', numero, 'es primo')
	else:
		print(numero, 'NO es primo')

	numeros = [1, 3, 6, 5113, 10226, 15339, 30678, 5093947]
	for i in numeros:
		if prime.isPrime(i):
			print('El numero', i, 'es primo')
		else:
			print(i, 'NO es primo')

	print(len(prime.primes), 'números primos almacenados en memoria')
	print('Números primos calculados hasta', prime.lastCalc,
			hex(prime.lastCalc))

##	prime.chkWithFermat()

	prime.svCSV()
##	print(fermat(2097143, 1))

##	k = 1024
##	p = prime.randomPrimeKBits(k)
##	print('Primo de', k,'Bits', p, bin(p))

	print('\nTiempo consumido: ', datetime.now() - born)

if __name__ == '__main__':
    #main()
    print(fermat(40403, 3))
