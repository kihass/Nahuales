##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
__author__ =	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ =   "$Version: 1 Revision: 1 Since: 06/03/14"
__project__ =   'DduC'
__doc__ =   	'Crea una copia de seguridad de los archivos con la ' + \
				'extension indicada, en base a la fecha de modificaci\'on'
__copyright__ = '© Kihass 2014'
__licence__ =   'GPLv3'
#-------------------------------------------------------------------------------
# $Source$


import os
import time
import shutil
from datetime import timedelta


def backup(ext):
	dateFormat = '%Y%m%d-%H%M%S'
	dirBackups = 'backups'

	if not os.path.isdir(dirBackups):
		os.mkdir(dirBackups)

	lenExt = len(ext)

	for fn in os.listdir("."):

		if fn[len(fn) - lenExt - 1: ] == ".%s" % ext:
			timestamp = time.strftime(dateFormat,
					time.localtime(os.path.getmtime(fn)))
			filename = fn[0: len(fn) - lenExt - 1]
			filename = '%s_%s.%s' % (filename, timestamp, ext)
			pathfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
					dirBackups, filename)

			if not os.path.exists(pathfile):
				print('Respaldando: "%s"' % fn, timestamp)
				inF = os.path.join(os.path.dirname(os.path.abspath(__file__)),
						fn)
				shutil.copy2(inF, pathfile)


def main():
	backup('py')
	backup('bat')
	backup('tex')
	backup('py')
	backup('bat')
	backup('tex')
	backup('odt')
	backup('bib')


if __name__ == '__main__':
	main()
