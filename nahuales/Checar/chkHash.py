##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         chkHash.py
# Purpose:      'Obtener el hash de todos los archivos del directorio actual'
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 14/08/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$
import hashlib
import os

print('\t\tHASH\t\t\t', '\t  File Name\n', '-' * 60)

for fn in os.listdir('.'):

	if os.path.isfile(fn):
		BLOCKSIZE = 65536
		hasher = hashlib.sha1()

		with open(fn, 'rb') as afile:
		    buf = afile.read(BLOCKSIZE)

		    while len(buf) > 0:
		        hasher.update(buf)
		        buf = afile.read(BLOCKSIZE)

		print(hasher.hexdigest(), '\t', fn)