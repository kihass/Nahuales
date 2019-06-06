##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Kike
#
# Created:     24/10/2013
# Copyright:   (c) Kike 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import threading
import multiprocessing
##from multiprocessing import Process
from multiprocessing import Process, Lock
import time
import os
import random
import sys


import MyECC
import Primos
import random
import MyECDSA


class TEST(object):
	__schema = 'dduc'
	__user = 'dduc'  # Ã‚Â¡Ya sÃƒÂ©! no los encripte a propÃƒÂ³sito -_-
	__passwd = 'dduc'  # " " " " "
	__mysql = {
			'user': __user,
			'password': __passwd,
			'host': '127.0.0.1',
			'database': __schema}
	__cores = multiprocessing.cpu_count()
	__critical = [0 for i in range(__cores)]


	def __init__(self):
		pass


	def testMySQL(self):
		""" Encuentra el ÃƒÂºltimo evento """
		#import pymysql
		import mysql
		import mysql.connector
##		conn = mysql.connector.connect(user=self.__user, password=self.__passwd,
##                              host='127.0.0.1',
##                              database=self.__schema)
		conn = mysql.connector.connect(**self.__mysql)
		cur = conn.cursor()
		cur.execute('SELECT * FROM tc_mr WHERE Evento = 1;')
		for i in cur:
			buffer = [None]
			for j in range(0, len(i)):
				buffer.append(None)
				buffer[j] = i[j]
			print('buffer %s' % buffer)
		cur.close()
		conn.close()


	def myThread(self):
		start = time.time()

		lock = threading.Lock()  # lock.acquire()     lock.release()
		hilos = self.__cores
		t = [None for i in range(hilos)]
		for i in range(hilos):
			parameters = {'cores': hilos, 'thread': i, 'Otro': None, 'lock': lock}
			t[i] = MyThread(self.eval, parameters)

		for i in range(hilos):
			t[i].start()

		for i in range(hilos):
			t[i].join()

		print('Terminando hilo principal')
		print(self.__critical)

		end = time.time()
		print("\nDuration: {0:.3f}s\n".format(end -start)) # una simple resta


	def myMultiProccesing(self):  # http://docs.python.org/3.3/library/multiprocessing.html
		start = time.time()

		lock = Lock()  # lock.acquire()     lock.release()
		hilos = self.__cores
		mp = [None for i in range(hilos)]
		for i in range(hilos):
			parameters = {'cores': hilos, 'thread': i, 'Otro': None, 'lock': lock}
			mp[i] = Process(target=self.eval, args=(parameters,))

		for i in range(hilos):
			mp[i].start()

		for i in range(hilos):
			mp[i].join()

		print('Terminando hilo principal')
		print(self.__critical)

		end = time.time()
		print("\nDuration: {0:.3f}s\n".format(end -start)) # una simple resta


	def eval(self, argParameters):
		print('Evaluando hilo %s' % argParameters['thread'])
		for i in range(10000000):
			self.__critical[argParameters['thread']] += 1
		print('Terminando hilo %s' % argParameters['thread'])


class MyThread(threading.Thread):
	""" Genera hilos para ejecutar la funciÃƒÂ³n indicada """

	def __init__(self, argFunction, argParameters):
		threading.Thread.__init__(self)

		self.function = argFunction
		self.parameters = argParameters
		self.numThread = self.parameters['thread']


	def run(self):
		""" Ejecuta la funciÃƒÂ³n en el hilo dado """
		self.function(self.parameters)


def prueba():
##	tst = TEST()
##	tst.myThread()
##	tst.myMultiProccesing()
##	print('Number of arguments:', len(sys.argv), 'arguments.')
##	print('Argument List:', str(sys.argv))

	b = 0b110000
	r = 0b10000

	if b > r:
		print('menor')
	else:
		if b == r:
			print('igual')
		else:
			print('mayor')

if __name__ == '__main__':
	prueba()
