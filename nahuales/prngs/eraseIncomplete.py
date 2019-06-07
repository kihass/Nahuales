import os
import sys

deadList = []
sizeMask = 1028016 // 8

flaErase = False

for arg in sys.argv:
	if arg == '-erase':
		flaErase = True

for dir in ('analysis',):
	for fn in os.listdir(dir):
		if fn[-7:] == ".report":
			fullFn = '{}/{}'.format(dir, fn)

			with open(fullFn, mode='r') as file:
				flaPreserve = False

				while True:
					buffer = file.readline()

					if not buffer:
						break

					if 'SUMMARY' in buffer:
						flaPreserve = True

					if '1,028,016 bits required' in buffer:
						print('Reporte fallido (mascara pequeña): {}'.format(fullFn))

						if flaErase:
							deadList.append(fullFn)

						break

				if not flaPreserve:
					print('Reporte incompleto: {}'.format(fullFn))

					if flaErase:
						if fullFn not in deadList:
							deadList.append(fullFn)

				file.close()

	for fn in os.listdir(dir):
		if fn[-5:] == ".mask":
			statinfo = os.stat('{}/{}'.format(dir,fn))

			if statinfo.st_size != sizeMask:
				print('Mascara incompleta: {} vs {} (dif {}) {}'.format(sizeMask, statinfo.st_size, statinfo.st_size - sizeMask, fn))

				if flaErase:
					print('Borrando: {}/{}'.format(dir, fn))
					os.remove("{}/{}".format(dir, fn))

for f in deadList:
	print('Borrando: {}'.format(f))
	os.remove("%s" % f)
