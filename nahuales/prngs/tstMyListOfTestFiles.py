#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Tester tools list of files"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2019"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 15/02/2019"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
# External librarie
from os import stat
from os.path import exists
from random import shuffle
from shutil import copy
from sys import path as syspath

syspath.append('..')

# Project libraries
from myBytesTools import bytes2int

keysSize = 25
minPValue = 0.01
# sizeOfTheStream=1048576
sizeOfTheStream = 1008000
sizeOfTheStream4Performance = 1000000

keys = [bytes([i % 256] if i // 256 == 0 else [i % 256, i // 256])
		for i in range(keysSize)]


class FilesNames(object):
	__files = [
		'https://www.random.org/analysis/Analysis2005.pdf',
		'data/originals/data.pi.bin',
		# https://gist.github.com/jsdario/6d6c69398cb0c73111e49f1218960f79
		'data/originals/VeraCrypt.key',
		'data/originals/sts-2_1_2.zip',
		'data/originals/cryptopp565.zip',
		'data/originals/Manglar.jpg',
		'data/originals/Kuky.jpg',
		'data/originals/nistspecialpublication800-22r1a.pdf',
		'data/originals/librotmed.pdf',
		'data/originals/Logo_Kike.png',
		'data/originals/Glider.png',
		'data/originals/gcc.1',
		'data/originals/g77.1',
		'data/originals/cpp.1',
		# C:\MinGW\man
		'data/originals/el_quijote.txt',
		'data/originals/randtest.py',
		'data/originals/nahual.py',
		'data/originals/dpbprw.py',
		'data/originals/data.pi',
		'data/originals/data.e',
	]
	__currentFileName = ''

	def alias(self):
		fn = self.fileNameFull()

		if fn == 'nistspecialpublication800-22r1a.pdf':
			return 'SP800-22r1a.pdf'
		else:
			return fn

	def eval(self):
		fn = "data/analize/{}".format(self.fileNameFull())
		fnHatch = "data/analize/{}.hatch".format(self.fileNameFull())
		fnOriginal = self.originals()

		# Check size
		statInfo = stat(fnOriginal)

		if statInfo.st_size > sizeOfTheStream:
			if not exists(fnHatch):
				print('Too big {}, hatch!'.format(fnOriginal))
				tmpData = b''

				with open(fnOriginal, mode='rb') as file:
					tmpData = file.read(sizeOfTheStream)
					file.close()

				with open(fnHatch, mode='wb') as file:
					file.write(tmpData)
					file.close()

			return fnHatch
		else:
			if not exists(fn):
				print('Copy {}'.format(fnOriginal))
				copy(fnOriginal, fn)

			return fn

	def extension(self):
		fn, ext = self.fileNameAndExt()
		return ext

	def fileName(self):
		fn, ext = self.fileNameAndExt()
		return fn

	def fileNameAndExt(self):
		name, ext = splitext(self.fileNameFull())
		return name, ext[1:]

	def fileNameFull(self):
		return basename(self.__currentFileName)

	def mask(self, argId: str, argKey: bytes):
		return "data/{}/{}-[{}].mask".format(argId, self.fileNameFull(),
		bytes2int(argKey))

	def maskReport(self, argId: str, argKey: bytes):
		return "data/{}/{}-[{}].report".format(argId, self.fileNameFull(),
		bytes2int(argKey))

	def originals(self):
		return 'data/originals/{}'.format(self.fileNameFull())

	def report(self):
		return "{}.report".format(self.eval())

	def scrollFileNames(self):
		for fn in self.__files:
			self.__currentFileName = fn
			yield fn

	def shuffleFiles(self):
		shuffle(self.__files)


if __name__ == '__main__':
	"""Example of use"""
	# This block is to be able to use the sample code at the end of the file
	# External libraries
	from sys import path as syspath
	from os import system
	from os.path import basename
	from os.path import dirname
	from os.path import splitext
	import platform

	syspath.append('..')

	# Project libraries

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	files = FilesNames()
	files.shuffleFiles()

	for fn in files.scrollFileNames():
		print(fn)
		print(files.fileNameAndExt())
		print(files.fileName())
		print(files.extension())
		print(files.fileNameFull())
		print(files.originals())
		print(files.report())
		print(files.alias())
		print(files.mask('id', b'123'))
		print(files.maskReport('id', b'123'))
		print(splitext(basename(fn))[1][1:])
		
		path = dirname(fn)
		fn, ext = splitext(basename(fn))
		ext = ext[1:]
		print(fn, ext, path)
		print()
