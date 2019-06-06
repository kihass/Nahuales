##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        myDES.py
# Purpose:     Elaborar una implementación del algoritomo de cifrado DES
#
# Author:      Kike
#
# Created:     27/08/2013
# Copyright:   (c) Kike 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math

class MY_DES(object):


	tE = (
			32,	1,	2,	3,	4,	5,  #  0- 5
			4,	5,	6,	7,	8,	9,  #  6-11
			8,	9,	10,	11,	12,	13, # 12-17
			12,	13,	14,	15,	16,	17, # 18-23
			16,	17,	18,	19,	20,	21, # 24-29
			20,	21,	22,	23,	24,	25, # 30-35
			24,	25,	26,	27,	28,	29, # 36-41
			28,	29,	30,	31,	32,	1)  # 42-47
	tPC_1 = ( # LEFT
			57,	49,	41,	33,	25,	17,	9,	#  0- 6
			1,	58,	50,	42,	34,	26,	18,	#  7-13
			10,	2,	59,	51,	43,	35,	27,	# 14-20
			19,	11,	3,	60,	52,	44,	36,	# 21-27
			# RIGHT
			63,	55,	47,	39,	31,	23,	15,	# 28-34
			7,	62,	54,	46,	38,	30,	22,	# 35-41
			14,	6,	61,	53,	45,	37,	29,	# 42-48
			21,	13,	5,	28,	20,	12,	4)	# 49-55
	tLS = (
			1,1,2,2,2,2,2,2,  # 1-8
			1,2,2,2,2,2,2,1)  # 9-16
	tPC_2 = (
			14,	17,	11,	24,	1,	5,	3,	28,	#  0- 7
			15,	6,	21,	10,	23,	19,	12,	4,  #  8-15
			26,	8,	16,	7,	27,	20,	13,	2,  # 16-23
			41,	52,	31,	37,	47,	55,	30,	40, # 24-31
			51,	45,	33,	48,	44,	49,	39,	56, # 32-39
			34,	53,	46,	42,	50,	36,	29,	32) # 40-47
	tS1 = (
			(14,	4,	13,	1,	2,	15,	11,	8,	3,	10,	6,	12,	5,	9,	0,	7),
			( 0,	15,	7,	4,	14,	2,	13,	1,	10,	6,	12,	11,	9,	5,	3,	8),
			( 4,	1,	14,	8,	13,	6,	2,	11,	15,	12,	9,	7,	3,	10,	5,	0),
			(15,	12,	8,	2,	4,	9,	1,	7,	5,	11,	3,	14,	10,	0,	6,	13))
	tS2 = (
			(15,	1,	8,	14,	6,	11,	3,	4,	9,	7,	2,	13,	12,	0,	5,	10),
			( 3,	13,	4,	7,	15,	2,	8,	14,	12,	0,	1,	10,	6,	9,	11,	5),
			( 0,	14,	7,	11,	10,	4,	13,	1,	5,	8,	12,	6,	9,	3,	2,	15),
			(13,	8,	10,	1,	3,	15,	4,	2,	11,	6,	7,	12,	0,	5,	14,	9))
	tS3 = (
			(10,	0,	9,	14,	6,	3,	15,	5,	1,	13,	12,	7,	11,	4,	2,	8),
			(13,	7,	0,	9,	3,	4,	6,	10,	2,	8,	5,	14,	12,	11,	15,	1),
			(13,	6,	4,	9,	8,	15,	3,	0,	11,	1,	2,	12,	5,	10,	14,	7),
			( 1,	10,	13,	0,	6,	9,	8,	7,	4,	15,	14,	3,	11,	5,	2,	12))
	tS4 = (
			( 7,	13,	14,	3,	0,	6,	9,	10,	1,	2,	8,	5,	11,	12,	4,	15),
			(13,	8,	11,	5,	6,	15,	0,	3,	4,	7,	2,	12,	1,	10,	14,	9),
			(10,	6,	9,	0,	12,	11,	7,	13,	15,	1,	3,	14,	5,	2,	8,	4),
			( 3,	15,	0,	6,	10,	1,	13,	8,	9,	4,	5,	11,	12,	7,	2,	14))
	tS5 = (
			( 2,	12,	4,	1,	7,	10,	11,	6,	8,	5,	3,	15,	13,	0,	14,	9),
			(14,	11,	2,	12,	4,	7,	13,	1,	5,	0,	15,	10,	3,	9,	8,	6),
			( 4,	2,	1,	11,	10,	13,	7,	8,	15,	9,	12,	5,	6,	3,	0,	14),
			(11,	8,	12,	7,	1,	14,	2,	13,	6,	15,	0,	9,	10,	4,	5,	3))
	tS6 = (
			(12,	1,	10,	15,	9,	2,	6,	8,	0,	13,	3,	4,	14,	7,	5,	11),
			(10,	15,	4,	2,	7,	12,	9,	5,	6,	1,	13,	14,	0,	11,	3,	8),
			( 9,	14,	15,	5,	2,	8,	12,	3,	7,	0,	4,	10,	1,	13,	11,	6),
			( 4,	3,	2,	12,	9,	5,	15,	10,	11,	14,	1,	7,	6,	0,	8,	13))
	tS7 = (
			( 4,	11,	2,	14,	15,	0,	8,	13,	3,	12,	9,	7,	5,	10,	6,	1),
			(13,	0,	11,	7,	4,	9,	1,	10,	14,	3,	5,	12,	2,	15,	8,	6),
			( 1,	4,	11,	13,	12,	3,	7,	14,	10,	15,	6,	8,	0,	5,	9,	2),
			( 6,	11,	13,	8,	1,	4,	10,	7,	9,	5,	0,	15,	14,	2,	3,	12))
	tS8 = (
			(13,	2,	8,	4,	6,	15,	11,	1,	10,	9,	3,	14,	5,	0,	12,	7),
			( 1,	15,	13,	8,	10,	3,	7,	4,	12,	5,	6,	11,	0,	14,	9,	2),
			( 7,	11,	4,	1,	9,	12,	14,	2,	0,	6,	10,	13,	15,	3,	5,	8),
			( 2,	1,	14,	7,	4,	10,	8,	13,	15,	12,	9,	0,	3,	5,	6,	11))
	tS = (tS1, tS2, tS3, tS4, tS5, tS6, tS7, tS8)
	tP = (
			16,	7,	20,	21,	29,	12,	28,	17, #  0- 7
			1,	15,	23,	26,	5,	18,	31,	10, #  8-14
			2,	8,	24,	14,	32,	27,	3,	9,  # 15-21
			19,	13,	30,	6,	22,	11,	4,	25) # 22-28
	tIP = (
			58,	50,	42,	34,	26,	18,	10,	2,  #  0- 7
			60,	52,	44,	36,	28,	20,	12,	4,  #  8-14
			62,	54,	46,	38,	30,	22,	14,	6,  # 15-21
			64,	56,	48,	40,	32,	24,	16,	8,  # 22-28
			57,	49,	41,	33,	25,	17,	9,	1,  # 29-35
			59,	51,	43,	35,	27,	19,	11,	3,  # 36-42
			61,	53,	45,	37,	29,	21,	13,	5,  # 43-49
			63,	55,	47,	39,	31,	23,	15,	7)  # 50-56
	tFP = (
			40, 8,	48,	16,	56,	24,	64,	32,	#  0- 7
			39,	7,	47,	15,	55,	23,	63,	31, #  8-14
			38,	6,	46,	14,	54,	22,	62,	30, # 15-21
			37,	5,	45,	13,	53,	21,	61,	29, # 22-28
			36,	4,	44,	12,	52,	20,	60,	28, # 29-35
			35,	3,	43,	11,	51,	19,	59,	27, # 36-42
			34,	2,	42,	10,	50,	18,	58,	26, # 43-49
			33,	1,	41,	9,	49,	17,	57,	25) # 50-56
	tSubKeys = []
	subKeys = 16
	cycles = 16


	def __init__(self):
		pass


	def des(self, argData, argKey):
		# Construye las subclaves
		self.__mkKeys(argKey)

##		cData = 0
##		for sD in range(math.ceil(len(argData) / 32)):
		choiceF = True
##		data = self.pI(argData >> sD * 64)
		data = argData
		block = [data & 0xFFFFFFFF, (data >> 32)]
		for cycle in self.cycles:
			block[(0,1)[choiceF]] ^= f(cycle, block[(1,0)[choiceF]])
			choiceF = not(choiceF)
		data = self.pF(block[0] | (block[1] << 32))
##		cData |= data << sD * 32
##		return cData
		return data


	def f(self, argRound, argData):
		# Función de Feistel (32 bits)
		# E ^ sKey
		tmpIn = self.e(argData) ^ self.tSubKeys[argRound]

		# S box's
		tmpOut = 0
		for s in range(8):
			tmpOut |= self.s((tmpIn >> (8 - s) * 6) & 0b111111) << (8 - s) * 4

		# P
		return self.p(tmpOut)  # (32 bits)


	def __mkKeys(self, argKey):
		# Construye las subclaves
		tmpKey = self.pc_1(argKey)
		b1 = tmpKey & int('1' * 28, 2)
		b2 = tmpKey & int('1' * 28 + '0' * 28, 2)
		for i in range(self.subKeys):
			b2, b1 = self.ls(i, b2, b1)
			self.tSubKeys.append(self.pc_2(b2, b1))


	def s(self, argBox, argData):
		# Permutaciones para cajas S (6 Bits)
		#print(bin(argData))  # debbug
		col = (argData >> 1) & 0b1111
		row = (argData & 0b1) | ((argData >> 4) & 0b10)
		#print('col:', bin(col))  # debbug
		#print('row:', bin(row))  # debbug
		return self.tS[argBox][row][col]  # (4 bits)


	def pc_2(self, argB2, argB1):
		# Permutación PC2 (2 x 28 bits)
##		data = ((argB2 & 0xFFFFFFF) << 28) | argB1 & 0xFFFFFFF
		data = (argB2 << 28) | argB1
		tmpPC2 = 0
		cont = 0
##		cont = 48 - 1
		for i in self.tPC_2:
			tmp = ((data >> i - 1) & 0b1) << cont
			#print('\t%s\t%s\t%s' % (cont, i, tmp))  # debbug
			tmpPC2 |= tmp
##			cont -= 1
			cont += 1
		return tmpPC2  # (48 bits)


	def ls(self, argRound, argB2, argB1):
		# Deslizamiento circular izquierdo (2 x 24 bits)

		def circularSlip(argSlip, argData):
			# Deslizamiento circular izquierdo (24 bits)
			slip2 = 28 - argSlip
			maskSlip = int('1' * slip2, 2)  # 28 - slip

			# (32 bits)
			return ((argData & maskSlip) << argSlip) | (argData >> slip2)

		slip = self.tLS[argRound]
		# (2 x 24 bits)
		return circularSlip(slip, argB2), circularSlip(slip, argB1)


	def pc_1(self, argData):
		# Permutación PC1 (64 bits)
		tmpPC1 = 0
		cont = 56 - 1
		for i in self.tPC_1:
			tmp = ((argData >> (i - 1)) & 0b1) << cont
			#print('\t%s\t%s\t%s' % (cont, i, tmp))  # debbug
			tmpPC1 |= tmp
			cont -= 1
		return tmpPC1  # (56 bits)


	def e(self, argData):
		# Función inicial (32 bits)
		tmpE = 0
		cont = 48 - 1
		for i in self.tE:
			tmp = ((argData >> (i - 1)) & 0b1) << cont
			#print('\t%s\t%s\t%s' % (cont, i, tmp))  # debbug
			tmpE |= tmp
			cont -= 1
		#print(bin(tmpE))  # debbug
		return tmpE  # (48 bits)


	def p(self, argData):
		# Permutación inicial (32 bits)
		tmpP = 0
		cont = 32 - 1
		for i in self.tP:
			tmp = ((argData >> i - 1) & 0b1) << cont
			#print('\t%s\t%s\t%s' % (cont, i, tmp))  # debbug
			tmpP |= tmp
			cont -= 1
		return tmpP  # (32 bits)


	def pF(self, argData):
		# Permutación inicial (64 bits)
		tmpFP = 0
		cont = 64 - 1
		for i in self.tFP:
			tmp = ((argData >> i - 1) & 0b1) << cont
			#print('\t%s\t%s\t%s' % (cont, i, tmp))  # debbug
			tmpFP |= tmp
			cont -= 1
		return tmpFP  # (64 bits)


	def pI(self, argData):
		# Permutación inicial (64 bits)
		tmpIP = 0
		cont = 64 - 1
		for i in self.tIP:
			tmp = ((argData >> i - 1) & 0b1) << cont
			#print('\t%s\t%s\t%s' % (cont, i, tmp))  # debbug
			tmpIP |= tmp
			cont -= 1
		return tmpIP  # (64 bits)


def main():
	myDES = MY_DES()
	myDES.des(b'1',b'1')


if __name__ == '__main__':
	main()