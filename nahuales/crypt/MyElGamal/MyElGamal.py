##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MyElGamal
# Purpose:     Implementación de algoritmo de firma digital de ElGamal sobre F_2
#
# Author:      ISC. Carlos Enrique Quijano Tapia
#
# Created:     05/11/2013
# Copyright:   (c) Kike 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------


import random
import Primos


def readFile(archivo):
	""" Lee un archivo y lo convierte en una cadena binaria """
	with open(archivo, mode='rb') as file:
		read = file.read()
		file.close()
	return read


def SHAfa(message):
	""" Digestor SHAfa """
	suma = [0,0]

	flag = True
	for text in message:
		if flag:
			suma[0] += text
		else:
			suma[1] += text
		flag = not flag

	suma[0] *= suma[1]
	suma[1] *= suma[0]

	suma[0] %= 256	# Corrección con respecto a C
	suma[1] %= 256	# Corrección con respecto a C

##	print(suma[1], suma[0])
	return 256 * suma[1] + suma[0]


def h(m):
	return SHAfa(m)


def evalPol(pol, Zp, α):
	bms = bitMoreSignificative(pol)
	result = 0

	for i in range(bms + 1):
		if (pol >> bms) & 0b1 == 1:
			result += α ** bms
		bms -= 1
	return result % Zp


def fastExponentαTable(a, k, table):
	""" Exponenciación rápida """
	A = a
	bms = bitMoreSignificative(k) - 2

	while bms >= 0:
		# A ^ 2
		αPowA = fndPowα(table, A)
		A = table[(αPowA + αPowA) % len(table)][1]

		# Extraer bit
		if (k >> bms) & 0b1 == 1:
			# A * a
			αPowA = fndPowα(table, A)
			αPowa = fndPowα(table, a)
			A = table[(αPowA + αPowa) % len(table)][1]

		bms -= 1

	return A


def prodα(A, B, table):
	αPowA = fndPowα(table, A)
	αPowB = fndPowα(table, B)

	return table[(αPowA + αPowB) % len(table)][1]


def fastExponentPol_2(a, k, p):
	""" Exponenciación rápida """
	A = a
	bms = bitMoreSignificative(k) - 2

	while bms >= 0:
		# A ^ 2
		A = modPol_2(prodPol_2(A, A), p)

		# Extraer bit
		if (k >> bms) & 0b1 == 1:
			# A * a
			A = modPol_2(prodPol_2(A, a), p)

		bms -= 1

	return A


def fastExponent(a, k):
	""" Exponenciación rápida """
	A = a
	bms = bitMoreSignificative(k) - 2

	while bms >= 0:
		# A ^ 2
		A *= A
##
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
		A = (A * A) % Zp
##
		# Extraer bit
		if (k >> bms) & 0b1 == 1:
			# A * a
			A = (A * a) % Zp

		bms -= 1

	return A


def fndPowα(table, pol):
	result = None
	for i in table:
		if pol == i[1]:
			result = i[0]
	return result


def gcd(a,b):
	""" Máximo comun divisor por el algoritmo extendido de Euclides """
	if b == 0:
		return a
	else:
		return gcd(b, a % b)


def gcdPol(a,b):
	""" Máximo comun divisor por el algoritmo extendido de Euclides """
	if b == 0:
		return a
	else:
		return gcdPol(b, modPol_2(a, b))


def egcd(a, b):
	""" Encuentra el máximo comun divisor aplicando el algoritmo extendido de
	Euler.
	http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python"""
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)


def egcdPol(a, b):
	""" Encuentra el máximo comun divisor aplicando el algoritmo extendido de
	Euler.
	http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python"""
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcdPol(modPol_2(b, a), a)
		return (g, x + prodPol_2(divPol_2Int(b, a), y), y)  # TODO SURE


def divPol_2Int(a, b, q = 0b0):
	""" División, para polinomios expresados como cadenas binarias """
	if a < b:
		return q
	else:
		# Obtenemos el bit más significativo
		if a > b:
			bms = bitMoreSignificative(a)
		else:
			bms = bitMoreSignificative(b)
		# Dividimos A
		for d in range(bms):
			bd = b << d
			r = a ^ bd
			if bd > r:
				q ^= (1 << d)
				return divPol_2Int(r, b, q)


def divPol_2(a, b, q = 0b0):
	""" División, para polinomios expresados como cadenas binarias """
	if a < b:
		return q, a
	else:
		# Obtenemos el bit más significativo
		if a > b:
			bms = bitMoreSignificative(a)
		else:
			bms = bitMoreSignificative(b)
		# Dividimos A
		for d in range(bms):
			bd = b << d
			r = a ^ bd
			if bd > r:
				q ^= (1 << d)
				return divPol_2(r, b, q)


def multiplicativeInverse(z, Zp):
	""" Encuentra z^-1 aplicando el algoritmo extendido de Euler """
	g, t, y = egcd(z, Zp)
	if g != 1:
		print(z, bin(z))
		raise Exception('modular inverse does not exist')
	else:
		return t % Zp


def multiplicativeInversePol(k, qm):
	""" Encuentra z^-1 aplicando el algoritmo extendido de Euler """
	g, t, y = egcdPol(k, qm)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		result = modPol_2(t, qm)
		if modPol_2(prodPol_2(k, result), qm) == 1:
			return result
		else:
			print('Falló el inverso polinomial, buscando por fuerza bruta')
			result = 0
			for i in range(qm):
				result += 1
				if modPol_2(prodPol_2(k, result), qm) == 1:
					return result
##				if result % 1024 == 0:
##					print(result, bin(result))


def multiplicativeInverseα(k, table):
	""" Encuentra z^-1 aplicando el algoritmo extendido de Euler """
	print('Buscando el inverso por fuerza bruta')
	for i in table:
		result = i[1]
		if prodα(k, result) == 1:
			result
		return result
	print('No se encontó el inverso')


def bitMoreSignificative(num):
	""" Obtiene el bit mas significativo de un numero binario """
	bms = 0
	while True:
		if 2 ** bms > num:
			break
		bms += 1
	return bms


def modPol_2(a, b):
	""" Operación módulo, para polinomios expresados como cadenas binarias """
	if a < b:
		return a
	else:
		# Obtenemos el bit más significativo
		if a > b:
			bms = bitMoreSignificative(a)
		else:
			bms = bitMoreSignificative(b)
		# Busca divisor
		for d in range(bms):
			bd = b << d
			r = a ^ bd
			# Sí divide (el residúo es menor que el divisor)
			if bd > r:
				# Vuelve a dividir el residuo
				return modPol_2(r, b)


def divPol_2(a, b, q = 0b0):
	""" División, para polinomios expresados como cadenas binarias """
	if a < b:
		return q, a
	else:
		# Obtenemos el bit más significativo
		if a > b:
			bms = bitMoreSignificative(a)
		else:
			bms = bitMoreSignificative(b)
		# Dividimos A
		for d in range(bms):
			bd = b << d
			r = a ^ bd
			if bd > r:
				q ^= (1 << d)
				return divPol_2(r, b, q)


def addPol_2(a, b):
	""" Adición poliomial, para polinomios expresados como cadenas binarias """
	return a ^ b


def prodPol_2(a, b):
	""" Producto polinomal, para polinomios expresados como cadenas binarias """
	# Verificamos si podemos reducir operaciones intercambiando datos
	if a > b:
		tmp = a
		a = b
		b = tmp

	# Obtenemos el bit mas significativo
	bms = bitMoreSignificative(a)

	# Recorremos el la cadena binaria
	c = 0b0
	for slide in range(bms + 1):
		# Verificamos que el bit este encendido
		if (a >> slide) & 0b1 == 1:
			# Deslizamos y agregamos a c
			c ^= b << slide
	return c


def prodPol_GF2(a, b, GF):
	""" Producto polinomal, para polinomios expresados como cadenas binarias """
	# Verificamos si podemos reducir operaciones intercambiando datos
	if a > b:
		tmp = a
		a = b
		b = tmp

	# Obtenemos el bit mas significativo
	bms = bitMoreSignificative(a)

	# Recorremos el la cadena binaria
	c = 0b0
	for slide in range(bms + 1):
		# Verificamos que el bit este encendido
		if (a >> slide) & 0b1 == 1:
			# Deslizamos y agregamos a c
			c ^= modPol_2(b << slide, GF)
	return c


def buildαTable_2(iPol, q, m):
	""" Genera tabla de potencias de α para campos finitos q^m """
	qm = q ** m
	bms = bitMoreSignificative(iPol)
	basis = modPol_2(iPol, 1 << bms - 1)
	bmsBasis = bitMoreSignificative(basis)
	table = []
	for α in range(qm - q + 1):
		if α < bms - 1:
			table.append((α, 1 << α))
		elif α == (bms - 1):
			table.append((α, basis))
		else:
			newα = prodPol_2(0b10, table[α - 1][1])
			newα = modPolαTable_2(table, newα)
			table.append((α, newα))

	print('0\t', bin(0), '   \t', hex(0))   # DEBUGG
	for row in table[:20]:   # DEBUGG
		print("a^%s" % row[0], '\t', bin(row[1]), '   \t', hex(row[1]))	# DEBUGG
	print('...')
	tmp = len(table) - 1
	for row in table[tmp - 2:tmp]:   # DEBUGG
		print("a^%s" % row[0], '\t', bin(row[1]), '   \t', hex(row[1]))	# DEBUGG

	return table


def modPolαTable_2(table, pol):
	""" Reemplaza los polinomios coeficientes de los polinomios binários, por
	los de la tabla """
	bms = bitMoreSignificative(pol)
	p = len(table)

	# Recorremos la cadena binaria
	result = 0b0
	for s in range(bms + 1):
		# Verificamos que el bit este encendido
		if (pol >> s) & 0b1 == 1:
			result ^= table[s % p][1]
	return result


def factors(n):
	return [i for i in range(1, n // 2 + 1) if not n % i] + [n]


def primeAndGeneratorZp(k, t, Zp):
    # 1. Repeat the following:
	prime = Primos.PRIME()
	p = None
	while True:
		# 1.1 Select a random k-bit prime p (for example, using Algorithm 4.44).
		while True:
			p = random.randint(t, k)
			if bitMoreSignificative(p) <= 16 and prime.isPrime(p):
				break

		# 1.2 Factor p − 1.
		theFactors = [i for i in range(t, (p-1) // 2 + 1) if not (p-1) % i] + [p-1]
		# Until p − 1 has a prime factor >= t.
		exists = False
		for i in theFactors:
			if i >= t:
				exists = True
				break
		if exists:
			break
	# 2. Use Algorithm 4.80 with G = Z*_p and n = p − 1 to find a generator
	# alpha of Z*_p
	α = 2
	# 3. Return(p, alpha)
	return p, α


class ELGAMAL(object):


	a = None
	GF = None


	def generateKeys(self, qm, π, table):
		""" Key generation for the ElGamal signature scheme """
		# SUMMARY: each entity creates a public key and corresponding private
		# key. Each entity A should do the following:
		self.table = table

		# 1. Generate a large random prime p and a generator alpha of the
		# multiplicative group Z*_p (using Algorithm 4.84 Selecting a k-bit
		# prime p and a generator alpha of Z*_p).
##		p = None
##		p = π
##		α = None
##		prime = Primos.PRIME()
##		while True:
##			p = random.randint(1, qm - 1)
##			p = prime.randomPrimeKBits(bitMoreSignificative(qm - 1))    # INT:
##			if Primos.fermat(p, 10):
##			if Primos.fermat(p, 10) and gcdPol(p, π) == 1:
##				break
		p = 2 ** 16
##		α = ... # TODO: hacer en implementación final
		α = 2

		# 2. Select a random integer a, 1 <= a <= p − 2.
##		a = ...	# TODO: hacer en implementación final
		a = 12345
		self.a = a

		# 3. Compute y = alpha^a mod p (e.g., using Algorithm 2.143).
##		y = fastExponentZp(α, a, p) # INT
##		y = fastExponentαTable(α, a, table) % p
##		y = modPol_2(fastExponentαTable(α, a, table), p)
		y = fastExponentαTable(α, a, table)

		# 4. A’s public key is (p, alpha, y); A’s private key is "a".
		return p, α, y


	def sign(self, p, α, y, msg):
		""" Signature generation. Entity A should do the following """
		# (a) Select a random secret integer k, 1 <= k <= p − 2, with
		# gcd(k, p − 1) = 1.
##		k = None
##		while True:
##			k = random.randint(1, p - 2)
##			if gcd(k, p - 1) == 1:	# INT
##			if gcdPol(k, p - 1) == 1 and gcd(k, p - 1):
##				break
		k = 11

		# (b) Compute r = alpha^k mod p (e.g., using Algorithm 2.143).
##		r = fastExponentZp(α, k, p)	# INT
##		r = fastExponentαTable(α, k, self.table) % p
##		r = fastExponentPol_2(α, k, p)
##		r = modPol_2(fastExponentαTable(α, k, self.table), p)
		r = fastExponentαTable(α, k, self.table)

		# (c) Compute k^{−1} mod (p − 1) (e.g., using Algorithm 2.142).
		hm = h(msg)
		invK = multiplicativeInverse(k, p - 1)  # INT
##		invK = multiplicativeInversePol(k, p - 1)
##		invK = multiplicativeInverseα(k, table)
##		print('invk = ', invK, bin(invK))   # DEBUG

		# (d) Compute s = k^{−1}{h(msg) − a*r} mod (p − 1).
		ar = self.a * r		# INT
##		ar = prodα(self.a, r, self.table)
##		ar = prodPol_GF2(self.a, r, self.GF)
		hm_ar = hm - ar
##		hm_ar = hm ^ ar
##		hm_ar = modPol_2(hm_ar, self.GF)
		s = (invK * hm_ar) % (p - 1)	# INT
##		s = prodPol_2(invK, hm_ar) % (p - 1)
##		s = modPol_2(prodPol_2(invK, hm_ar), p - 1)
##		s = prodα(invK, hm_ar, self.table)
##		s = prodPol_GF2(invK, hm_ar, self.GF)

		# (e) A’s signature for msg is the pair (r, s).
		return r, s


	def verification(self, p, α, y, r, s, msg):
		""" Verification. To verify A’s signature (r, s) on msg, B should do the
		following: """
		# (a) Obtain A’s authentic public key (p, alpha, y).

		# (b) Verify that 1 <= r <= p − 1; if not, then reject the signature.
		if 1 <= r <= p - 1:

			# (c) Compute v1 = y^r * r^s mod p.
			yr = fastExponentZp(y, r, p)    # INT
##			yr = fastExponent(y, r)
##			yr = fastExponentαTable(y, r, self.table)
##			yr = modPol_2(y ** r, p)
##			yr = modPolαTable_2(self.table, yr)
##			yr = fastExponentPol_2(y, r, p)
			rs = fastExponentZp(r, s, p)    # INT
##			rs = fastExponent(r, s)
##			rs = fastExponentαTable(r, s, self.table)
##			rs = modPol_2(r ** s, p)
##			rs = modPolαTable_2(self.table, rs)
##			rs = fastExponentPol_2(r, s, p)
			v1 = (yr * rs) % p	# INT
##			v1 = yr * rs
##			v1 = modPol_2(yr * rs, p)
##			v1 = modPol_2(prodPol_2(yr, rs), p)
##			v1 = modPolαTable_2(self.table, prodPol_2(yr, rs))
##			v1 = prodα(yr, rs, self.table)
##			v1 = prodPol_GF2(yr, rs, self.GF)

			# (d) Compute h(msg) and v2 = alpha^{h(msg}} mod p.
			hm = h(msg)
			v2 = fastExponentZp(α, hm, p)   # INT
##			v2 = fastExponent(α, hm)
##			v2 = fastExponentαTable(α, hm, self.table) % p
##			v2 = modPol_2(fastExponentαTable(α, hm, self.table), p)
##			v2 = fastExponentαTable(α, hm, self.table)

			# (e) Accept the signature if and only if v1 = v2.
			print('y^r = %s %s, r^s = %s %s,\nv1 = %s %s, v2 = %s %s' %
					(yr, bin(yr), rs, bin(rs), v1, bin(v1), v2, bin(v2)))
			if v1 == v2:
				print('VERIFICADO')
				return True
			else:
				print('No Verificado')
				return False
		else:
			print('Firma rechazada')
			return False


def eval():
	##    65432109876543210
	π = 0b10010100001000001
	q = 2
	m = 16
	α = 2
	a = 12345
	k = 11

	msg = readFile('Documento')
	table = None
	table = buildαTable_2(π, q, m)
	egm = ELGAMAL()
	egm.GF = 2 ** 16

	# Calcula el orden -> 2^16 -1
##	result = fastExponentαTable(0b10, 2 ** 16 - 1, table)
##	print('Comprobamos alpha ^ (2^16 - 1):\t', evalPol(result, q ** m, α),
##			'\tPolinomio:\t', bin(result))

	while True:
		# Obtener y = alpha^α
		print('\nGenerando llaves')
		print('GF(q^m) = GF(%s^%s) =' % (q, m), q ** m, ',',
				bitMoreSignificative(q ** m - 2), 'bits:')
		p, α, y = egm.generateKeys(q ** m, π, table)
		print('y =', y, bin(y), bitMoreSignificative(y))
		print('alpha =', α, bin(α), bitMoreSignificative(α))
		print('p =', p, bin(p), bitMoreSignificative(p))

		# Firmar doc r y s
		print('\nFirmando')
		r, s = egm.sign(p, α, y, msg)
		print('r =', r, bin(r), ', s =', s, bin(s))

		# Encontrar r, s, y^r, r^s, v1 y v2
		print('\nVerificando')
		flaTerminar = egm.verification(p, α, y, r, s, msg)
		if flaTerminar:
			break
		else:
			break

def main():
##	qm = 2 ** 16
##	print(qm, bin(qm), bitMoreSignificative(qm))
##	qm = 2 ** 16 - 1
##	print(qm, bin(qm), bitMoreSignificative(qm))
##	qm = (2 ** 16) % (2 ** 16)
##	print(qm, bin(qm), bitMoreSignificative(qm))
	eval()

if __name__ == '__main__':
    main()
