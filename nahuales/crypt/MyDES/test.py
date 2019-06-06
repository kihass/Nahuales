##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Kike
#
# Created:     29/08/2013
# Copyright:   (c) Kike 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from myDES import MY_DES


def tstPC_2():  # 56 bits
	myDES = MY_DES()
	for i in myDES.tPC_2:
		num = 0b1 << i - 1
		b2 = num >> 28
		b1 = num & 0xFFFFFFF
		print('%s\t%s' % (i, bin(myDES.pc_2(b2, b1))))  # debbug

	myIn = int('1'*24, 2) << 24
	print('\n\t%s' % bin(myIn))
	for i in myDES.tPC_2:
		num = 0xFFFFFFF << 28
		b2 = num >> 28
		b1 = num & 0xFFFFFFF
		print('%s\t%s' % (i, bin(myDES.pc_2(b2, b1))))  # debbug

	print('\n\t%s' % bin(myIn))
	for i in myDES.tPC_2:
		num = 0xFFFFFFF
		b2 = num >> 28
		b1 = num & 0xFFFFFFF
		print('%s\t%s' % (i, bin(myDES.pc_2(b2, b1))))  # debbug


def tstPC_1():  # 64 bits
	myDES = MY_DES()
	for i in myDES.tPC_1:
		num = 0b1 << i - 1
		print('%s\t%s' % (i, bin(myDES.pc_1(num))))  # debbug

def tstE():
	myDES = MY_DES()
	for i in myDES.tE:
		num = 0b1 << i - 1
		print('%s\t%s' % (i, bin(myDES.e(num))))  # debbug

def tstIP():
	myDES = MY_DES()
	for i in myDES.tIP:
		num = 0b1 << i - 1
		print('%s\t%s' % (i, bin(myDES.pI(num))))  # debbug

def tstFP():
	myDES = MY_DES()
	for i in myDES.tFP:
		num = 0b1 << i - 1
		print('%s\t%s' % (i, bin(myDES.pF(num))))  # debbug

def tstP():
	myDES = MY_DES()
	for i in myDES.tP:
		num = 0b1 << i - 1
		print('%s\t%s' % (i, bin(myDES.p(num))))  # debbug

def tstLS():
	myDES = MY_DES()
	b1 = 1
	b2 = 1 << 1
	for i in range(len(myDES.tLS)):
		b1, b2 = myDES.ls(i, b1, b2)
		print('%s\t%s\t%s\n\t\t%s' % (i, myDES.tLS[i], bin(b1), bin(b2)))  # debbug

def mkHexTablesPC2():
	myDES = MY_DES()
	pc2 = [[[0] for data in range(256)] for bloque in range(8)]
	for bloque in range(8):
		for data in range(256):
			tmp56 = data << bloque * 7
			b1 = (tmp56 & 0xFFFFFFF)
			b2 = (tmp56 >> 28) & 0xFFFFFFF
			tmp48 = myDES.pc_2(b2, b1)
			tmpOut = 0
			for sb in range(8):
				tmpOut |= ((tmp48 >> sb * 6) & 0b111111) << sb * 8
##			pc2[bloque][data] = (tmpOut >> (1,0)[bloque >= 4] * 32) & 0xFFFFFFFF  # POrque solo al revez
			pc2[bloque][data] = (tmpOut >> (0,1)[bloque >= 4] * 32) & 0xFFFFFFFF
##			pc2[bloque][data] = tmpOut

	with open('output.csv', 'w') as file:
		contB = 0
		for bloque in pc2:
			file.write('PC2_Tab_%s\n' % contB)
			output = []
			cont = 0
			for data in bloque:
				subStr = '%x' % data
				subStr = '0x%s%s' % (('0' * (8 - len(subStr))), subStr)
				output.append(subStr)
				if cont == 7:
					output = '%s,\n' % output
					output = output.replace('[', '')
					output = output.replace(']', '')
					output = output.replace("'", '')
					file.write(output)
					output = []
					cont = 0
				else:
					cont += 1
			file.write('\n\n')
			contB += 1


def main():
	tstPC_2()
	tstPC_1()
	tstE()
	tstIP()
	tstFP()
	tstP()
	tstLS()
	mkHexTablesPC2()

if __name__ == '__main__':
    main()

