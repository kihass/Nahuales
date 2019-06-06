#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Encryption example"""

__author__ = 'M. en C. Carlos Enrique Quijano Tapia (kike.qt@gmail.com)'
__copyright__ = "(c) Carlos Enrique Quijano Tapia 2018"
__credits__ = ""

__licence__ = "GPLv3"
__version__ = "$Version: 0 Revision: 0 Since: 20/02/2018"
__maintainer__ = "Carlos Enrique Quijano Tapia"
__email__ = "kike.qt@gmail.com"
__status__ = "Developing"

# $Source$
import sys

from nahual import NAHUAL

if __name__ == '__main__':
	flaFK = False
	flaInputFile = False
	flaOutputFile = False
	flaSetKey = False
	sizeMask = 0

	cipher = NAHUAL()

	for arg in sys.argv:
		if arg[: 3] == 'if=':
			cipher.loadMsg(arg[3:])
			flaInputFile = True

		elif arg[: 4] == 'key=':
			cipher.key = arg[4:]
			flaSetKey = True

		elif arg[: 9] == 'keyFiles=':
			cipher.setFilesKey(arg[9:].split(','))
			flaFK = True

		elif arg[: 9] == 'sizeMask=':
			sizeMask = int(arg[9:])

		elif arg[: 3] == 'of=':
			cipher.outputFile = arg[3:]
			flaOutputFile = True

		elif arg == 'cipher.py':
			pass

		else:
			print(arg, "Is it well written?")
			exit()

	if not flaSetKey:
		cipher.captureKey()
		flaSetKey = True

	if sizeMask == 0:
		if flaFK and flaInputFile and flaOutputFile and flaSetKey:
			cipher.run()

		else:
			if not flaFK:
				print("Missing define the key file")

			if not flaInputFile:
				print("Missing the input file")

			if not flaOutputFile:
				print("Missing the output file")

			if not flaSetKey:
				print(
					"Fatal error: the encryption key has not been defined",
					"(This should never happen)"
				)
	else:
		cipher.mask(sizeMask)
