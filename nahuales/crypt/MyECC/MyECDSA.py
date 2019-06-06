##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        ECDSA.py
# Purpose:     Implementación de firma digital
#
# Author:      ISC. Carlos Enrique Quijano Tapia
#
# Created:     30/10/2013
# Copyright:   (c) Kike 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------


import MyECC
import random


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


class ECDSA(object):


	E = None	# Coeficientes de la curva eliptica
	P = None    # Punto racional de orden N
	n = None	# Campo finito
	Ϭ = (-1,-1) # Punto al infinito
	d = None    # d
	Q = None    # Q
	ecc = None  # Criptografía de Curvas Elípticas


	def generateKeys(self, argE, P, Zp, d, Ϭ = (-1,-1)):
		""" Proceso de generación de firmas """
		self.ecc = MyECC.ECC()
		self.ecc.Zp = Zp
		self.ecc.Ϭ = Ϭ

        # Paso 1: Seleccione una curva elíptica E.
		self.ecc.E = argE

        # Paso 2: Seleccione un punto P (que pertenezca a E) de orden n.
		self.ecc.P = P
		self.P = P
		self.n = self.ecc.order(self.P)

		# Paso 3: Seleccione aleatoriamente un número d en el intervalo
		# [1, n - 1].
##		self.d = random.randint(1, self.n - 1)
		self.d = d  # TODO Sólo para este ejemplo

        # Paso 4: Calcule Q = dP.
		self.Q = self.ecc.fndQ(d, P)

		# Paso 5: d será la llave privada.
		# Paso 6. Q será la llave pública.
		return self.d, self.Q


	def sign(self, m, k = None):
		""" Proceso de firma digital """
##		k = None
		kP = None
		r = None
		s = None
		invK = None
		while True:
            # Paso 1: Seleccione un número k de forma aleatoria
##			k = random.randint(1, self.n - 1)
            # Paso 2: Calcule kP = (x_1,y_1).
			kP = self.ecc.fndQ(k, self.ecc.P)
            # Paso 3:  Calcule r = x_1 mod n. Si r = 0 regresa al primer paso.
			# (En este paso x_1 es tratado como un entero).
			r = kP[0] % self.n
			if kP[0] != 0:
		        # Paso 4: Calcule (k^{-1}) mod n.
				invK = MyECC.multiplicativeInverse(k, self.n)

				# Paso 5: Calcule s = k^{-1}(H(m) + dr) mod n. Si s = 0 regrese
				# al primer paso. (H(m) es el hash del mensaje a firmar,
				# calculado con el algoritmo SHA-1).
				s = (invK * (SHAfa(m) + self.d * r)) % self.n  # TODO despues cambiarlo origen
				if s != 0:
					break
		# Paso 6: La firma del mensaje m son los números r y s.
		return r, s


	def verification(self, m, r, s):
		""" Proceso de verificación """
		# Paso 1. Verifique que r y s estén dentro del rango [1,n - 1].
		r = r % self.n
		s = s % self.n

		# Paso 2. Calcule w = s^{-1} mod n.
		w = MyECC.multiplicativeInverse(s, self.n) % self.n
		# Paso 3. Calcule u_1 = H(m)w mod n.
		u_1 = (SHAfa(m) * w) % self.n
		# Paso 4. Calcule u_2 = r·w mod n.
		u_2 = (r * w) % self.n
		# Paso 5. Calcule u_{1}P + u_{2}Q = (x_0,y_0)
		uP = self.ecc.fndQ(u_1, self.ecc.P)
		uQ = self.ecc.fndQ(u_2, self.Q)
		myXY = self.ecc.addition(uP, uQ)
		# Paso 6. Calcule v = x_0 mod n
		v = myXY[0] % self.n
		# Paso 7. La firma verifica sí y solo sí v = r
		if v == r:
			print('Verificado')
			print('\tv = %s, w = %s,\n\tu1 = %s, u2 = %s,\n\tu1*P = %s,u2*Q = %s'
				% (v, w, u_1, u_2, uP, uQ))
		else:
			print('No válido')


def main():
	P = (27230, 28427)
	d = 123
	E = (1,0,1,1)
	Zp = 30677
	k = 555

	ecc = MyECC.ECC()
	ecc.E = E
	ecc.Zp = Zp
	print('kP =', ecc.fndQ(k, P))

	# Generamos llaves
	ecdsa = ECDSA()
	d, Q = ecdsa.generateKeys(E, P, Zp, d)

	m = readFile('Documento')
	print('SHAfa =', SHAfa(m))

	# Firmamos
	r, s = ecdsa.sign(m, k)
##	r, s = ecdsa.sign(m)
	print('r =', r, ', s =', s)

	# Verificación
	ecdsa.verification(m, r, s)


if __name__ == '__main__':
    main()
