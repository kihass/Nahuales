#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Unitary tests"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
from hashlib import sha1
from os import path
from os import system
import unittest

if __name__ == '__main__':
	from sys import path as syspath
	syspath.append('..')

	from myBytesTools import activeBits
	from myBytesTools import bin2Str
	from myBytesTools import binStr2Bytes
	from myBytesTools import bytes2BitIter
	from myBytesTools import bytes2DecimalPart
	from myBytesTools import bytes2int
	# from myBytesTools import float2bytes
	from myBytesTools import int2bytes
	from myBytesTools import readBit
	from myBytesTools import rol
	from myBytesTools import ror
	from myBytesTools import xor4bytes
	from myCircularFileSynthesizer import Circular_File_Synthesizer
	from myBytesTools import myByteOrder
	from nahual import NAHUAL

else:
	from nahuales.myBytesTools import activeBits
	from nahuales.myBytesTools import bin2Str
	from nahuales.myBytesTools import bytes2BitIter
	from nahuales.myBytesTools import bytes2DecimalPart
	from nahuales.myBytesTools import bytes2int
	# from nahuales.myBytesTools import float2bytes
	from nahuales.myBytesTools import int2bytes
	from nahuales.myBytesTools import readBit
	from nahuales.myBytesTools import rol
	from nahuales.myBytesTools import ror
	from nahuales.myBytesTools import xor4bytes
	from nahuales.myCircularFileSynthesizer import Circular_File_Synthesizer
	from nahuales.myTools import myByteOrder
	from nahuales.nahual import NAHUAL


class Test_Complete(unittest.TestCase):
	"""Unit tests for the Nahuales project"""
	def test_Msg(self):
		"""Testing for messages"""
		if not path.exists('tests/1.txt'):
			with open('tests/1.txt', mode='w') as file:
				file.write('1')
				file.close()

		self.nahual = NAHUAL()
		self.nahual.msg2Str = "hello world"

		self.assertEqual(self.nahual.msg2Bin, 0x68656c6c6f20776f726c64)
		self.assertEqual(self.nahual.msg2Hex, "68656c6c6f20776f726c64".lower())
		self.assertEqual(self.nahual.msg2Str, "hello world")
		self.assertEqual(
			chr(self.nahual.msg2Bytes[0]) + chr(self.nahual.msg2Bytes[1]), "he"
		)

		self.nahual.loadMsg('tests/1.txt')
		self.assertEqual(self.nahual.msg2Bytes, b'1')

	def test_Hash(self):
		"""Tests to check hash usage"""
		myHash = sha1(str.encode("hello world"))
		self.assertEqual(
			myHash.hexdigest(),
			"2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
		)
		self.assertEqual(
			int.from_bytes(myHash.digest(), myByteOrder),
			0x2aae6c35c94fcfb415dbe95f408b9ce91ee846ed
		)

		myHash = sha1()
		myHash.update(str.encode("hello world"))
		self.assertEqual(
			myHash.hexdigest(),
			"2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
		)
		self.assertEqual(
			int.from_bytes(myHash.digest(), myByteOrder),
			0x2aae6c35c94fcfb415dbe95f408b9ce91ee846ed
		)

	def test_Bytes(self):
		"""Usage tests and concepts of data types Bytes"""
		for myInt in range(256):
			self.assertEqual(len(int2bytes(myInt)), 1)

		myBinVal = 0x68656C6C6F7720776F726C64
		self.assertEqual(
			int2bytes(myBinVal), str.encode("hellow world")
		)

		# TODO(No sé como verificar esta información)
		# myFloat = 3.14159
		# myFloatInBin = float2bytes(myFloat)
		# print(bytes(myFloatInBin))
		# print(bin(bytes2int(myFloatInBin)))
		# print(bin(int.from_bytes(myFloatInBin, "little")))
		# self.assertEqual(myFloat, )

		self.assertEqual(len(str.encode("hello world")), 11)

	def tests_myBytesTools(self):
		"""Library tests myBytesTools"""
		myXorData = xor4bytes(
			str.encode("hello world"), str.encode("012345678901")
		)
		myXorData = xor4bytes(myXorData, str.encode("012345678901"))
		self.assertEqual(myXorData, str.encode("hello world"))

		# Nota: recordar que la representación de bits se hace en little endian
		self.assertEqual(0.0, bytes2DecimalPart(int2bytes(0b0)))
		self.assertEqual(0.5, bytes2DecimalPart(int2bytes(0b1)))
		self.assertEqual(0.25, bytes2DecimalPart(int2bytes(0b10)))
		self.assertEqual(0.75, bytes2DecimalPart(int2bytes(0b11)))
		self.assertEqual(0.125, bytes2DecimalPart(int2bytes(0b100)))
		self.assertEqual(0.625, bytes2DecimalPart(int2bytes(0b101)))
		self.assertEqual(
			0.001953125, bytes2DecimalPart(int2bytes(0b100000000))
		)

		# For details please see the documentation of activeBitsIterable
		self.assertEqual(activeBits(b'@ABC'), [0, 1, 6, 9, 14, 16, 22, 30])

		for pos in activeBits(b'@ABC'):
			self.assertEqual(readBit(b'@ABC', pos), 1)

		vActive = activeBits(b'@ABC')

		for pos in range(len(b'@ABC') * 8):
			if pos in vActive:
				self.assertEqual(readBit(b'@ABC', pos), 1)
			else:
				self.assertEqual(readBit(b'@ABC', pos), 0)

		vTest = [
			0b01000000010000010100001001000011,
			0b10100000001000001010000100100001,
			0b11010000000100000101000010010000,
			0b01101000000010000010100001001000,

			0b00110100000001000001010000100100,
			0b00011010000000100000101000010010,
			0b00001101000000010000010100001001,
			0b10000110100000001000001010000100,

			0b01000011010000000100000101000010,
			0b00100001101000000010000010100001,
			0b10010000110100000001000001010000,
			0b01001000011010000000100000101000,

			0b00100100001101000000010000010100,
			0b00010010000110100000001000001010,
			0b00001001000011010000000100000101,
			0b10000100100001101000000010000010,

			0b01000010010000110100000001000001,
			0b10100001001000011010000000100000,
			0b01010000100100001101000000010000,
			0b00101000010010000110100000001000,

			0b00010100001001000011010000000100,
			0b00001010000100100001101000000010,
			0b00000101000010010000110100000001,
			0b10000010100001001000011010000000,
			
			0b01000001010000100100001101000000,
			0b00100000101000010010000110100000,
			0b00010000010100001001000011010000,
			0b00001000001010000100100001101000,

			0b00000100000101000010010000110100,
			0b00000010000010100001001000011010,
			0b00000001000001010000100100001101,
			0b10000000100000101000010010000110,
			]

		#print('org: ', bin2Str(bytes2int(b'@ABC')))

		for cycle in range(1, len(vTest)):
			#print('bin: ', bin2Str(bytes2int(ror(b'@ABC', cycle))))
			self.assertEqual(ror(b'@ABC', cycle), int2bytes(vTest[cycle]))

		for cycle in reversed(range(1, len(vTest))):
			#print('bin: ', bin2Str(bytes2int(ror(b'@ABC', cycle))))
			self.assertEqual(rol(b'@ABC', cycle), int2bytes(vTest[cycle]))

		vTest = [
					0, 1, 0, 0, 0, 0, 0, 0,
					0, 1, 0, 0, 0, 0, 0, 1,
					0, 1, 0, 0, 0, 0, 1, 0,
					0, 1, 0, 0, 0, 0, 1, 1,
				]
		pos = 0

		for cBit in bytes2BitIter(b'@ABC', 34):
			self.assertEqual(cBit, vTest[pos])
			pos += 1

		pos = 0

		for cBit in bytes2BitIter(b'@ABC', 10):
			self.assertEqual(cBit, vTest[pos])
			pos += 1

		pos = 0
		
		for cBit in bytes2BitIter(b'@ABC'):
			self.assertEqual(cBit, vTest[pos])
			pos += 1

		self.assertEqual(
				b'@ABC',
				binStr2Bytes('01000000 01000001 01000010 01000011')
			)

	def tests_myCircularFiles(self):
		"""Circular file library tests"""
		for i in range(1, 3 + 1):
			if not path.exists('tests/%s.txt' % i):
				with open('tests/%s.txt' % i, mode='w') as file:
					file.write(('%s' % i) * i)
					file.close()

		cfs = Circular_File_Synthesizer(
			['tests/1.txt', 'tests/2.txt', 'tests/3.txt']
		)
		self.assertEqual(cfs.data, b'122333')

		self.assertEqual(cfs.readInBytes(), b'1')
		self.assertEqual(cfs.readInBytes(), b'2')
		self.assertEqual(cfs.readInBytes(), b'2')
		self.assertEqual(cfs.readInBytes(), b'3')
		self.assertEqual(cfs.readInBytes(), b'3')
		self.assertEqual(cfs.readInBytes(), b'3')
		self.assertEqual(cfs.readInBytes(), b'1')
		cfs.jumpPos(1)

		self.assertEqual(cfs.readInBytes(2), b'23')
		cfs.readInBytes(4)
		self.assertEqual(cfs.readInBytes(2), b'23')
		self.assertEqual(cfs.readInBytes(13), b'3312233312233')


if __name__ == '__main__':
	import platform

	if platform.system() == 'Linux':
		system("clear")

	else:
		system("CLS")

	unittest.main()

	if platform.system() == 'Linux':
		system("read -rsp $'Press any key to continue...\n' -n 1 key")

	else:
		system("PAUSE")
