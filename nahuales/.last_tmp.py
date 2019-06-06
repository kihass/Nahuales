##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        tests_nahuales
# Purpose:     Pruebas unitarias
#
# Author:      M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)
#
# Created:     15/02/2018
# Copyright:   (c) Kike 2018
# Licence:     GPLv3
#-------------------------------------------------------------------------------
__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2018"
# $Source$

import hashlib
import os
import platform
import unittest

import nahuales
import myBytesTools
import myCircularFileLists
import myTools

class Test_Complete(unittest.TestCase):
	def test_Msg(self):
		if not os.path.exists('tests/1.txt'):
			with open('tests/1.txt', mode='w') as file:
				file.write('1')
				file.close()

		self.nahual = nahuales.NAHUAL()
		self.nahual.setMsgStr("hello world")
		self.assertEqual(self.nahual.getMsgBin(), 0x68656c6c6f20776f726c64)
		self.assertEqual(self.nahual.getMsgHex(), "68656c6c6f20776f726c64".lower())
		self.assertEqual(self.nahual.getMsgStr(), "hello world")
		self.assertEqual(chr(self.nahual.getMsgBytes()[0])+chr(self.nahual.getMsgBytes()[1]), "he")

		self.nahual.loadMsg('tests/1.txt')
		self.assertEqual(self.nahual.getMsgBytes(), b'1')


	def test_Hash(self):
		myHash = hashlib.sha1(str.encode("hello world"))
		self.assertEqual(myHash.hexdigest(), "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed")
		self.assertEqual(int.from_bytes(myHash.digest(), "big"), 0x2aae6c35c94fcfb415dbe95f408b9ce91ee846ed)

		myHash = hashlib.sha1()
		myHash.update(str.encode("hello world"))
		self.assertEqual(myHash.hexdigest(), "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed")
		self.assertEqual(int.from_bytes(myHash.digest(), "big"), 0x2aae6c35c94fcfb415dbe95f408b9ce91ee846ed)


	def test_Bytes(self):
		myBinVal = 0x68656C6C6F7720776F726C64
		self.assertEqual(myBytesTools.int2bytes(myBinVal), str.encode("hellow world"))

		# TODO No sé como verificar esta información
		#myFloat = 3.14159
		#myFloatInBin = myBytesTools.float2bytes(myFloat)
		#print(bytes(myFloatInBin))
		#print(bin(myBytesTools.bytes2int(myFloatInBin)))
		#print(bin(int.from_bytes(myFloatInBin, "little")))
		#self.assertEqual(myFloat, )

		self.assertEqual(len(str.encode("hello world")), 11)


	def tests_myBytesTools(self):
		myXorData = myBytesTools.xor4bytes(str.encode("012345678901"), str.encode("hello world"))
		myXorData = myBytesTools.xor4bytes(str.encode("012345678901"), myXorData)
		self.assertEqual(myXorData, str.encode("hello world"))


	def tests_myCircularFiles(self):
		for i in range(1,3+1):
			if not os.path.exists('tests/%s.txt' % i):
				with open('tests/%s.txt' % i, mode='w') as file:
					file.write(('%s' % i) * i)
					file.close()

		cf = myCircularFileLists.Circular_File_Lists(['tests/1.txt', 'tests/2.txt', 'tests/3.txt'])
		self.assertEqual(cf.getAllData(), b'122333')

		self.assertEqual(cf.readDataInBytes(), b'1')
		self.assertEqual(cf.readDataInBytes(), b'2')
		self.assertEqual(cf.readDataInBytes(), b'2')
		self.assertEqual(cf.readDataInBytes(), b'3')
		self.assertEqual(cf.readDataInBytes(), b'3')
		self.assertEqual(cf.readDataInBytes(), b'3')
		self.assertEqual(cf.readDataInBytes(), b'1')
		cf.jumpPos(1)
		
		self.assertEqual(cf.readDataInBytes(2), b'23')
		tmpTrash = cf.readDataInBytes(4)
		self.assertEqual(cf.readDataInBytes(2), b'23')
		self.assertEqual(cf.readDataInBytes(13), b'3312233312233')


if __name__ == '__main__':
	if platform.system() == 'Linux':
		os.system("clear")
		
	else:
		os.system("CLS")
		
	unittest.main()