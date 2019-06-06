##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MyAES.py
# Purpose:     Implementación del algoritmo AES
#
# Author:      ISC. Carlos Enrique Quijano Tapia
#
# Created:     25/10/2013
# Copyright:   (c) Kike 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class MyAES(object):


	Nb = 4  # Number of columns (32-bit words) comprising the State.
	Nk = None	# Number of 32-bit words comprising the Cipher Key. For this
				#standard, Nk = 4, 6, or 8.
	Nr = None	# Number of rounds, which is a function of Nk and Nb (which is
				# fixed). For this standard, Nr = 10, 12, or 14.
	K = None	# Cipher Key
	Rcon = []   # The round constant word array.
	irreduciblePolynomial = 0b100011011  # m(x) = x^8 + x^4 + x^3 + x +1,
	orderIP = 8
	sBox = [
            [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
			[0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
			[0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
			[0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
			[0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
			[0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
			[0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
			[0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
			[0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
			[0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
			[0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
			[0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
			[0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
			[0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
			[0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
			[0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
			]


	def __init__(self, kbr):
		self.hardness(kbr)


	def AddRoundKey(self):
		""" Transformation in the Cipher and Inverse Cipher in which a Round Key
		is added to the State using an XOR operation. The length of a Round Key
		equals the size of the State (i.e., for Nb = 4, the Round Key length
		equals 128 bits/16 bytes). """
		for i in range(16):
			state[i] ^= roundKey[i]
			
		return state


	def InvMixColumns(self):
		""" Transformation in the Inverse Cipher that is the inverse of
		MixColumns(). """
		pass


	def InvShiftRows(self):
		""" Transformation in the Inverse Cipher that is the inverse of
		ShiftRows(). """
		pass


	def InvSubBytes(self):
		""" Transformation in the Inverse Cipher that is the inverse of
		SubBytes(). """
		pass


	def RotWord(self):
		""" Function used in the Key Expansion routine that takes a four-byte
		word and performs a cyclic permutation. """
		pass


	def ShiftRows(self):
		""" Transformation in the Cipher that processes the State by cyclically
		shifting the last three rows of the State by different offsets."""
		pass


	def SubBytes(self):
		""" Transformation in the Cipher that processes the State using a
		nonlinear byte substitution table (S-box) that operates on each of the
		State bytes independently. """
		pass


	def SubWord(self):
		""" Function used in the Key Expansion routine that takes a four-byte
		input word and applies an S-box to each of the four bytes to produce an
		output word."""
		pass


	def bitMore(self, number):
		# Buscando el bit mas significativo
		bitMore = 0
		while number >= 2 ** bitMore:
			bitMore += 1
		return bitMore - 1


	def addition(self, A, B):
		""" Adición en el campo XOR """
		return A ^ B


	def multiplication(self, A, B):
		""" Multiplicación en el campo """
		multiplication = 0

		# Buscamos el bit mas significativo de B
		bitMore = self.bitMore(B)
##		print('A: %s, B: %s, Bits:' % (bin(A), bin(B)), bitMore)  # DEBUGG
		# Multitplica cada elemento
		while bitMore >= 0:
			# Leemos el bit de la posición actual
			bit = (B >> bitMore) & 0b1
##			print('bitMore: % s, bit:%s' % (bitMore, bit))  # DEBUGG
			if bit == 1:
##				print('pos:', bitMore)  # DEBUGG
				multiplication ^= A * 0b1 << bitMore
			bitMore -= 1

##		print('sub:', bin(multiplication))  # DEBUGG
		return self.modulo(multiplication)


	def modulo(self, Num):
		""" Operación módulo en el campo.  Rijndael's finite field
		http://en.wikipedia.org/wiki/Finite_field_arithmetic """

##		print('Mod(%s)' % Num)  # DEBUGG
		bitMore = self.bitMore(Num)

		while bitMore >= 8:  # self.orderIP = 8
			Num = Num ^ (self.irreduciblePolynomial << bitMore - 8) # self.orderIP = 8
			bitMore = self.bitMore(Num)
		return Num


	def multiplicativeInverse(self, z, Zp):
		""" Encuentra el inverso multiplicativo z^-1 """
		t = 1
		while not (t * z) % Zp == 1:
			t += 1
		return t


	def cipher(self, myIn, myOut, word):
		""" Crifrado por bloque. byte myIn[4*Nb], byte myOut[4*Nb], word
		w[Nb*(Nr+1)] """
##			byte state[4,Nb]
##			state = in
##			AddRoundKey(state, w[0, Nb-1]) // See Sec. 5.1.4
##			for round = 1 step 1 to Nr–1
##				SubBytes(state) // See Sec. 5.1.1
##				ShiftRows(state) // See Sec. 5.1.2
##				MixColumns(state) // See Sec. 5.1.3
##				AddRoundKey(state, w[round*Nb, (round+1)*Nb-1])
##			end for
##			SubBytes(state)
##			ShiftRows(state)
##			AddRoundKey(state, w[Nr*Nb, (Nr+1)*Nb-1])
		out = state
		return out
##		end



	def hardness(self, kbr):
		""" Fortaleza del cifrado 128, 192 o 256 """
		if kbr == 128:
			self.Nk = 4
			self.Nr = 10
		elif kbr == 192:
			self.Nk = 6
			self.Nr = 12
		elif kbr == 256:
			self.Nk = 8
			self.Nr = 14
		else:
			print('Error Fatal: Variación inaceptable')
			exit(1)




def main():
	b = int(input("> "))
	aes = MyAES(b)
	# Vectores de prueba
	print('adicion:', bin(aes.addition(0b1010111, 0b10000011)), '[0b11010100]')
	print('adicion:', hex(aes.addition(0x57, 0x83)), '[0xd4]')
	print('módulo:', bin(aes.modulo(0b11111101111110)), '[0b1]')
	print('Multiplicación:', bin(aes.multiplication(0b1010111, 0b10000011)), '[0b11000001]')
	print('Multiplicación:', hex(aes.multiplication(0x57, 0x83)), '[0xc1]')
	print('Multiplicación:', hex(aes.multiplication(0x57, 0x13)), '[0xfe]')
	print('Multiplicación:', hex(aes.multiplication(0x57, 0x02)), '[0xae]')
	print('Multiplicación:', hex(aes.multiplication(0x57, 0x04)), '[0x47]')
	print('Multiplicación:', hex(aes.multiplication(0x57, 0x08)), '[0x8e]')
	print('Multiplicación:', hex(aes.multiplication(0x57, 0x10)), '[0x07]')
	print('Multiplicación:', bin(aes.multiplication(0b1111, 0b1111)), '[0x07]')
	# TODO Queda pendiente implementar XTIME Pág 15
	# TODO pag 19


def test():
	pass


if __name__ == '__main__':
	main()
##	test()