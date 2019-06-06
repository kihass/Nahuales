##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        TareaExamen2.py
# Purpose:     Exámen práctico de Criptografía
#
# Author:      ISC. Carlos Enrique Quijano Tapia
#
# Created:     22/10/2013
# Copyright:   (c) Kike 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------

import MyECC
import Primos
import random
import MyECDSA
from datetime import datetime


def eval(E, Zp, argP, argd):
	print('#' * 80)
	print('Iniciando: ', datetime.now())
	born = datetime.now()
	prime = Primos.PRIME()

	ecc = MyECC.ECC()
	ecc.E = E
	ecc.Zp = Zp

	ecc.Ϭ = (-1, -1)
	P = argP
	d = argd
	k = 555
	ecc.rp = [ecc.Ϭ]

	if ecc.ldPreCalc():
		pass
	else:
		ecc.findRationalPoints(ecc.E, ecc.Zp, ecc.Ϭ)
		ecc.svPreCalc()

	if ecc.isRationalPoints(ecc.E, ecc.Zp, P):
		print('\nP =', P , ' es un punto racional de los', len(ecc.rp), 'puntos')
		order = ecc.orderFast(P)
		print('\nCalculamos el orden como: Ord%s = %s' % (P, order))
		if prime.isPrime(order) and k < order:
			print('\nEl orden', order, 'es un número primo')
	else:
		print('\nP =', P ,' NO es un punto racional de los', len(ecc.rp))
		ecc.calcGen()
##		print('\nBuscándo un nuevo punto...')
		while True:
			P = ecc.rp[random.randint(1, len(ecc.rp) - 1)]
			order = ecc.orderFast(P)
			if prime.isPrime(order) and k < order:
				break
		print('\nEncontramos un nuevo punto P =', P, 'cuyo orden es',
				ecc.orderFast(P))
		##	print('Comprobación lenta: ', ecc.fndQSlow(d,P))

	Q = ecc.fndQ(d, P)
	print('\nSí d = %s y P = %s ->' % (d, P), ' Q =', Q)

##	# Calculamos el orden de los valores que falten
##	ecc.calcMassOrders()

	ecc.svData()

	ecdsa = MyECDSA.ECDSA()
	d, Q = ecdsa.generateKeys(ecc.E, P, ecc.Zp, d)
	m = MyECDSA.readFile('Documento')
	print('\nEl Hash SHAfa es %s (%s)' % (MyECDSA.SHAfa(m), hex(MyECDSA.SHAfa(m))))
	print('')
	r, s = ecdsa.sign(m, k)
	print('Al firmar obtuvimos: r =', r, 'y s =', s)
	print('')
	ecdsa.verification(m, r, s)

	print('\nTiempo consumido: ', datetime.now() - born)

def main():
##	eval((1,0,1,1), 30677, (1090,18593), 123)
	eval((1,1,0,1), 30677, (1090,18593), 123)

if __name__ == '__main__':
    main()
