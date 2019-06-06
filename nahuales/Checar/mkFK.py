##!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         chkHash.py
# Purpose:      'Construir un archivo llave, controlando los parametros clave '
__author__ = 	'Isc Carlos Enrique Quijano Tapia (kihass@yahoo.com.mx)'
__version__ = 	"$Version: 0 Revision: 0 Since: 21/08/14"
__project__ = 	'DduC'
__copyright__ =	'(c) Kihass 2014'
__licence__ =	'GPLv3'
#-------------------------------------------------------------------------------
# $Source$

import struct
from random import randint
from cipher import size

fkName = 'test/test.key'
sz = 0
with open(fkName, 'wb') as file:
	# Offset inicial
	for ins in range(0):  # No importa mucho ya que es un archivo circular
		file.write(struct.pack('>B', randint(0, 255)))

	# Construccion del gf para parametros
	for cell in range(256):
		sPsi = randint(1, 254)  # Tamano del conjunto de reglas para la celda
		file.write(struct.pack('>B', sPsi))

		for Psi in range(sPsi):
			# Seleccion de reglas, aqui se puede hacer que elija entre un
			# conjunto predefinido de reglas
			file.write(struct.pack('>B', randint(1, 254)))

	# Relleno final, apartir de aqui mkInstructions para obtener tokens
	# No importa mucho la extension ya que es un archivo circular
	for ins in range(randint(1, 1024)):
		file.write(struct.pack('>B', randint(1, 254)))

	file.close()

with open(fkName, 'rb') as file:
	sz = size(file)
	file.close()

print('Generando el archivo llave', fkName, ', %s bytes' % sz)