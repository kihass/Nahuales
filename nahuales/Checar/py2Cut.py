##!/usr/bin/python2
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         testVectors.py
# Purpose:      Corregir funciones cuya implementación previa no funciono
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 05/10/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


import os
import struct
import math


def main():
	for fn in os.listdir('data'):
		if fn[len(fn) - 11: ] == '.randomness':
			print(fn)
			results = []
			newResults = []
			with open('data/%s' % fn, mode='r') as file:
				results = file.readline()
				results = results.split(',')
				file.close()
			newResults.append(int(results[0]))
			newResults.append(results[1])
			newResults.append(float(results[2]))
			newResults.append(float(results[3]))
			newResults.append(float(results[4]))
			newResults.append(float(results[5]))
			newResults.append(float(results[6]))
			newResults.append(float(results[7]))
			newResults.append(float(results[8]))
			newResults.append(float(results[9]))
			newResults.append(float(results[10]))
			newResults.append(float(results[11]))
			newResults.append(float(results[12]))
			
			mySum = 0
			with open('data/%s' % fn, mode='w') as file:
				for i in [0,1,2,3,4,5,6,7,8,9,10,11,12]:
					file.write('%s,' % newResults[i])
				for i in [2,3,4,5,6,7,8,9,10,11,12]:
					mySum+=newResults[i]
				mySum = mySum / 11
				file.write('%s\n' % mySum)
				file.close()
			


if __name__ == '__main__':
    main()


