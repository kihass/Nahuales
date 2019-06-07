def lcg(a: int, c: int, M: int, argRequiredBytes: int):
	"""Linear Congruential Generators (LCG)
	a:	
	c:	Additive constant where gcd (c, M) = 1
	M:	Maximum expected period
	
	returns
	Xn:	Sequence of numbers

	c and m are relatively prime,
	a−1 is divisible by all prime factors of m
	a−1 is a multiple of 4 if m is a multiple of 4.
	"""
	Xn = 0

	for iteration in range(argRequiredBytes):
		Xn = (a * Xn + c) % M
		yield Xn / M


if __name__ == '__main__':
	"""Example of use"""
	# External libraries
	from fractions import gcd
	from os import system
	from os.path import basename
	import platform

	# Project libraries

	if platform.system() == 'Windows':
		system('CLS')

	else:
		system('clear')

	iam = basename(__file__)[:-3]
	print('Example of use by {}'.format(iam))
	
	for data in lcg(1140671485, 128201163, 2**24, 100):
		print(data)

	for data in lcg(1103515245, 12345, 2**32, 100):
		print(data)
