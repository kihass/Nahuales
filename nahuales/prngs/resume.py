from os import listdir
#from os import rename

if __name__ == '__main__':
	output = 'test,ext,file,pass,aprobed,,monobit_test,,frequency_within_block_test,,runs_test,,'
	output += 'longest_run_ones_in_a_block_test,,binary_matrix_rank_test,,dft_test,,'
	output += 'non_overlapping_template_matching_test,,overlapping_template_'
	output += 'matching_test,,maurers_universal_test,,linear_complexity_test,,'
	output += 'serial_test,,approximate_entropy_test,,cumulative_sums_test,,'
	output += 'random_excursion_test,,random_excursion_variant_test\n'

	for fn in listdir('analysis'):
		#if 'calc_' in fn:
		#	rename(fn, fn.replace('calc_', 'calc-dpbprw_'))
		#	continue

		if fn[-7:] == ".report":
			test = fn[fn.find('-') + 1 : fn.find('_')]

			ext = fn[fn.find('[') - 5: fn.find('[')]
			ext = ext[ext.find('_') + 1 :]

			fileMask = fn[fn.find('_') + 1 : fn.find('_{}'.format(ext))]

			password = fn[fn.find('[') + 1 : fn.find(']')]

			output += "{},{},{},{},".format(test, ext, fileMask, password)
			tmpOutput = ""

			tests = []

			cntPass = 0

			with open("analysis/{}".format(fn)) as file:
				print(fn)
				flaWait = True

				while True:
					buffer = file.readline()
						
					if not buffer:
						break

					if flaWait:
						if '-------' in buffer:
							flaWait = False
					else:
						for i in range(6):
							buffer = buffer.replace('  ', ' ').replace('\t', ' ')

						buffer = buffer.strip()
						buffer = buffer.split(' ')

						isPASS = True if float(buffer[1]) >= 0.01 else False
						cntPass += 1 if isPASS else 0

						#print(buffer[1], isPASS)

						tmpOutput += '{},{},'.format(buffer[1], 'PASS' if isPASS else 'FAIL')

			output += '{},{}\n'.format(cntPass, tmpOutput)

	with open('data/randomness_Summary.csv', mode='w') as file:
		file.write(output)
		file.close()
